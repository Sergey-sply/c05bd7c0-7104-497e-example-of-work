import asyncio
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import async_sessionmaker

from mail_domain_service.infrastructure.cache.redis.redis_job_cache import RedisJobCache
from mail_domain_service.infrastructure.cache.waiter_registry import waiters
from mail_domain_service.infrastructure.database import async_session_maker_ctx
from mail_domain_service.infrastructure.schemas.mailbox import MailboxMessage
from mail_domain_service.infrastructure.services.mailbox import MailService
from mail_domain_service.infrastructure.taskiq.tasks.get_mail import read_latest_task


log = logging.getLogger(__name__)

class GetLatestMail:
    def __init__(self, mail_service, job_cache: RedisJobCache, wait_default: float | None = 10.0):
        self.mail_service: MailService = mail_service
        self.cache = job_cache
        self.wait = wait_default
        self._session_maker: async_sessionmaker = async_session_maker_ctx.get()

    async def _get_mailbox_data(self, order_id: UUID):
        async with self._session_maker() as session:
            async with session.begin():
                mailbox = await self.mail_service.get_mail_data(
                    order_id=order_id,
                    session=session
                )
                return mailbox

    async def execute(self, order_id: UUID) -> MailboxMessage | dict:
        mailbox_data = await self._get_mailbox_data(order_id)

        res = await self.cache.get_result(str(order_id))
        if res:
            return await self._success_and_cleanup(order_id, res)

        # check task in queue
        if not await self.cache.is_inflight(str(order_id)):
            # set task in queue and mark as inflight for dedup
            if await self.cache.claim_inflight(str(order_id)):
                await read_latest_task.kiq(mailbox_data)

        # try to set or get waiter for this request
        fut = waiters.get_or_create(str(order_id))
        if fut is None:
            return MailboxMessage(
                status="too many requests",
                result="error",
                message=None
            )

        # wait by in-memory waiter
        try:
            payload = await asyncio.wait_for(fut, timeout=self.wait)
        except asyncio.TimeoutError:
            log.info("Timeout waiting worker response")

        # check cache for result
        res = await self.cache.get_result(str(order_id))
        if not res:
            return MailboxMessage(
                status="processing",
                result="processing",
                message=None
            )

        return await self._success_and_cleanup(order_id, res)

    async def _success_and_cleanup(self, order_id: UUID, res: MailboxMessage) -> MailboxMessage:
        async with self._session_maker() as session:
            async with session.begin():

                if res.result == "found" and res.message:
                    # mark mail as used
                    pass
                if res.status == "failed" and res.result == "error":
                    return res

                await self.cache.clear_result(str(order_id))
                await self.cache.clear_inflight(str(order_id))

                return res


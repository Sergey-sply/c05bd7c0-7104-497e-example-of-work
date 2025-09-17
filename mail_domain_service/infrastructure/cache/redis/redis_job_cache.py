import json
import logging
import time

from pydantic import ValidationError
from redis.asyncio import Redis
from typing_extensions import NoReturn

from mail_domain_service.infrastructure.cache.job_cache import JobCache
from mail_domain_service.infrastructure.schemas.mailbox import MailboxMessage


log = logging.getLogger(__name__)

class RedisJobCache(JobCache):
    def __init__(self, redis: Redis, inflight_ttl: int | None = None, result_ttl: int | None = 180):
        self.inflight_ttl = inflight_ttl
        self.result_ttl = result_ttl
        self.redis = redis

    def _inflight_key(self, order_id: str) -> str: return f"job:inflight:{order_id}"

    def _result_key(self, order_id: str) -> str:   return f"job:result:{order_id}"

    async def is_inflight(self, order_id: str) -> bool:
        return await self.redis.exists(self._inflight_key(order_id)) == 1

    async def claim_inflight(self, order_id: str) -> bool:
        ok = await self.redis.setnx(
            self._inflight_key(order_id),
            json.dumps({"status":"processing","ts":time.time()})
        )
        if ok:
            await self.redis.expire(self._inflight_key(order_id), self.inflight_ttl)
        return ok

    async def clear_inflight(self, order_id: str) -> None:
        await self.redis.delete(self._inflight_key(order_id))

    async def get_result(self, order_id: str) -> MailboxMessage | None:
        raw = await self.redis.get(self._result_key(order_id))
        if not raw:
            return None
        try:
            return MailboxMessage.model_validate_json(raw)
        except ValidationError as e:
            log.warning("Bad result payload in Redis for %s: %s", order_id, e)
            return None

    async def set_result(self, order_id: str, payload: MailboxMessage) -> NoReturn:
        """This method must be called in a worker"""
        await self.redis.set(self._result_key(order_id), payload.model_dump_json(), ex=self.result_ttl)

    async def clear_result(self, order_id: str) -> None:
        await self.redis.delete(self._result_key(order_id))

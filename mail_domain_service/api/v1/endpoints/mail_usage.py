from uuid import UUID

from fastapi import APIRouter

from mail_domain_service.api.schemas.mail import MailMessage
from mail_domain_service.application.use_cases.get_latest_mail import GetLatestMail
from mail_domain_service.infrastructure.cache.redis.client import get_redis
from mail_domain_service.infrastructure.cache.redis.redis_job_cache import RedisJobCache
from mail_domain_service.infrastructure.repositories.mailbox import MailRepository
from mail_domain_service.infrastructure.services.mailbox import MailService

mail_usage_router = APIRouter(
    prefix="/mail",
    tags=["mail"],
)


@mail_usage_router.get("/last", response_model=MailMessage)
async def get_latest_mail(
    order_uuid: UUID,
):
    redis = await get_redis()
    job_cache = RedisJobCache(redis=redis, inflight_ttl=60)
    # todo: use dishka container
    mail_repo = MailRepository()
    mail_service = MailService(mail_repo)
    mail_fetcher = GetLatestMail(
        mail_service=mail_service,
        job_cache=job_cache
    )

    latest_mail = await mail_fetcher.execute(
        order_id=order_uuid,
    )
    if latest_mail.status == "processing":
        return MailMessage(
        status="processing",
    )
    if latest_mail.result == "not found":
        return MailMessage(
            status="not found"
        )
    elif latest_mail.result == "error":
        return MailMessage(
            status="error"
        )
    message = latest_mail.message
    if message:
        return MailMessage(
            status="found",
            subject=message.subject,
            body=message.body,
            date=message.date
        )


from mail_reader_worker_example.app.cache.redis.provider import get_publisher
from mail_reader_worker_example.app.provider.base import MailProvider
from mail_reader_worker_example.app.schemas.mail import Mailbox
from mail_reader_worker_example.app.taskiq.broker import broker
from mail_reader_worker_example.app.use_case.mail_fetch import GetLatestMail


def provider_factory(provider_name: str) -> MailProvider:
    pass

@broker.task(task_name="read_latest_task")
async def read_latest(payload: Mailbox):
    get_latest_case = GetLatestMail(
        provider_factory=provider_factory
    )
    latest_mail = await get_latest_case.execute(mailbox=payload)

    publisher = await get_publisher()
    await publisher.publish(payload.order_id, latest_mail)
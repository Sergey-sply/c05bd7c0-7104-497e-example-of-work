import logging

from nats.js.api import StreamConfig
from taskiq import TaskiqMiddleware
from taskiq_nats import PullBasedJetStreamBroker

from mail_reader_worker_example.app.cache.redis.client import init_redis, close_redis
from mail_reader_worker_example.app.cache.redis.provider import reset_publisher
from mail_reader_worker_example.app.config.settings import settings

log = logging.getLogger(__name__)

broker = PullBasedJetStreamBroker(
    servers=[settings.NATS_BROKER_URL],
    durable=settings.js_durable,
    stream_name=settings.js_stream,
    subject=settings.js_subject,
    stream_config=StreamConfig(
        max_age=3600
    )
)

class BootstrapMiddleware(TaskiqMiddleware):
    async def startup(self) -> None:
        await init_redis()
        log.info("MailReader startup: Redis initialized.")

    async def shutdown(self) -> None:
        reset_publisher()
        await close_redis()
        log.info("MailReader shutdown: Redis closed.")

broker.add_middlewares(BootstrapMiddleware())
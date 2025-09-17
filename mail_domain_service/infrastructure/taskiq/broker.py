from nats.js.api import StreamConfig
from taskiq_nats import PullBasedJetStreamBroker

from mail_domain_service.config.settings import settings

broker = PullBasedJetStreamBroker(
    servers=[settings.NATS_BROKER_URL],
    durable=settings.js_durable,
    stream_name=settings.js_stream,
    subject=settings.js_subject,
    stream_config=StreamConfig(
        max_age=3600
    )
)
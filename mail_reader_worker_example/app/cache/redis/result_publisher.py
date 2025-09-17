from redis.asyncio import Redis

from mail_reader_worker_example.app.schemas.mail import MailboxMessage


class ResultPublisher:
    def __init__(self, redis: Redis, result_ttl: int = 180):
        self.result_ttl = result_ttl
        self.redis = redis

    @staticmethod
    def _result_key(order_id: str) -> str:
        return f"job:result:{order_id}"

    async def publish(self, order_id: str, msg: MailboxMessage) -> None:
        await self.redis.set(self._result_key(order_id), msg.model_dump_json(), ex=self.result_ttl)
        await self.redis.publish("job:result:bus", order_id)

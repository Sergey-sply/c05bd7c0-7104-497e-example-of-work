import asyncio
import json
import logging
from redis.asyncio import Redis

from mail_domain_service.infrastructure.cache.waiter_registry import waiters

log = logging.getLogger(__name__)

async def start_redis_listener(redis: Redis):
    pubsub = redis.pubsub()
    await pubsub.subscribe("job:result:bus")

    async def _runner():
        try:
            async for msg in pubsub.listen():
                t = msg.get("type")
                if t != "message":
                    continue
                try:
                    data = json.loads(msg["data"])
                    order_id = data.get("order_id")
                    if order_id:
                        waiters.resolve(order_id, {"wakeup": True})
                except Exception as e:
                    log.warning("Bad pubsub payload: %s", e)
                    pass
        except asyncio.CancelledError:
            pass

        except Exception as e:
            log.exception("PubSub listener crashed: %s", e)
            pass

        finally:
            # shutdown
            try:
                try:
                    await pubsub.unsubscribe("result:bus")
                except Exception:
                    pass
                await pubsub.close()
            except Exception:
                pass

    task = asyncio.create_task(_runner(), name="redis-result-listener")
    return task

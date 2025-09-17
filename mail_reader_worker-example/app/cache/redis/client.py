from redis.asyncio import Redis, ConnectionPool
from typing import Optional

from mail_reader_worker.app.config.settings import settings

_redis: Optional[Redis] = None

def build_pool() -> ConnectionPool:
    return ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASS,
        db=settings.REDIS_DB,
        max_connections=settings.REDIS_MAX_CONN,
        health_check_interval=30,
        socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
        socket_connect_timeout=settings.REDIS_CONNECT_TIMEOUT,
        retry_on_timeout=True,
    )

async def init_redis() -> Redis:
    global _redis
    if _redis is None:
        pool = build_pool()
        _redis = Redis(connection_pool=pool, decode_responses=True, encoding="utf-8")
    return _redis

async def get_redis() -> Redis:
    if _redis is None:
        raise
    return _redis  # type: ignore

async def close_redis():
    global _redis
    if _redis is not None:
        try:
            await _redis.close()
            await _redis.connection_pool.disconnect(inuse_connections=True)
        finally:
            _redis = None

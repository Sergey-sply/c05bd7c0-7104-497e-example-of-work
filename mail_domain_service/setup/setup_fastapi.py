from contextlib import asynccontextmanager

from fastapi import FastAPI

from mail_domain_service.infrastructure.cache.redis.client import get_redis, init_redis, close_redis
from mail_domain_service.infrastructure.taskiq.broker import broker
from mail_domain_service.setup import register_routers
from mail_domain_service.setup.redis_listener import start_redis_listener


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    await broker.startup()
    redis = await get_redis()
    app.state.task_listener = await start_redis_listener(redis)

    yield

    task = getattr(app.state, "task_listener", None)
    if task:
        task.cancel()

    await close_redis()
    await broker.shutdown()


def create_fastapi_app() -> FastAPI:
    app = FastAPI(
        title="Mail Usage Service",
        version="0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    register_routers(app)

    return app
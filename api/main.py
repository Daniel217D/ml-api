from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from redis.asyncio import Redis

from api.auth import verify_api_token
from api.container import Container
from api.endpoints.health.endpoints import router as health_router
from api.endpoints.tasks.endpoints import router as tasks_router
from api.endpoints.tasks_double.endpoints import router as tasks_double_router


def create_app() -> FastAPI:
    container = Container()
    settings = container.settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.redis = Redis.from_url(settings.redis_url, decode_responses=True)
        try:
            yield
        finally:
            await app.state.redis.aclose()

    app = FastAPI(
        title=settings.app_name,
        dependencies=[Depends(verify_api_token)],
        lifespan=lifespan,
    )

    app.container = container

    app.openapi_version = "3.0.3"
    app.include_router(health_router)
    app.include_router(tasks_double_router)
    app.include_router(tasks_router)

    return app


app = create_app()

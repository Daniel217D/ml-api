from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from api.auth import verify_api_token
from api.container import Container
from api.endpoints.health import endpoints as health_endpoints
from api.endpoints.tasks import endpoints as tasks_endpoints
from api.endpoints.tasks_double import endpoints as tasks_double_endpoints
from api.endpoints.health.endpoints import router as health_router
from api.endpoints.tasks.endpoints import router as tasks_router
from api.endpoints.tasks_double.endpoints import router as tasks_double_router


def create_app() -> FastAPI:
    container = Container()
    settings = container.settings()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            await container.redis().aclose()

    app = FastAPI(
        title=settings.app_name,
        dependencies=[Depends(verify_api_token)],
        lifespan=lifespan,
    )

    app.container = container
    container.wire(
        modules=[
            health_endpoints,
            tasks_endpoints,
            tasks_double_endpoints,
        ],
    )

    app.openapi_version = "3.0.3"
    app.include_router(health_router)
    app.include_router(tasks_double_router)
    app.include_router(tasks_router)

    return app


app = create_app()

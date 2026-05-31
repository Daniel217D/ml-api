from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from api.auth import verify_api_token
from api.common.responses import HealthResponse
from api.container import Container


def create_app() -> FastAPI:
    container = Container()
    settings = container.settings()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        yield

    app = FastAPI(
        title=settings.app_name,
        dependencies=[Depends(verify_api_token)],
        lifespan=lifespan,
    )
    app.container = container

    @app.get("/health", response_model=HealthResponse)
    def healthcheck() -> HealthResponse:
        return HealthResponse(status="ok")

    return app


app = create_app()

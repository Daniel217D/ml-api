from fastapi import Depends, FastAPI

from app.auth import verify_api_token
from app.common.responses import HealthResponse
from app.container import Container
from app.models import discover_routers


def create_app() -> FastAPI:
    container = Container()
    settings = container.settings()

    app = FastAPI(
        title=settings.app_name,
        dependencies=[Depends(verify_api_token)],
    )
    app.container = container

    for router in discover_routers():
        app.include_router(router)

    @app.get("/health", response_model=HealthResponse)
    def healthcheck() -> HealthResponse:
        return HealthResponse(status="ok")

    return app


app = create_app()

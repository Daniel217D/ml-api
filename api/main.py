from importlib import import_module
from pkgutil import iter_modules
from contextlib import asynccontextmanager
from types import ModuleType

from fastapi import Depends, FastAPI

from api.auth import verify_api_token
from api.common.logging import add_request_logging_middleware
from api.container import Container
from api import auth
from api import endpoints as endpoints_package


def discover_endpoint_modules() -> list[ModuleType]:
    modules: list[ModuleType] = []

    for module_info in sorted(
        iter_modules(endpoints_package.__path__),
        key=lambda item: item.name,
    ):
        if not module_info.ispkg:
            continue

        modules.append(import_module(f"api.endpoints.{module_info.name}.endpoints"))

    return modules


def create_app() -> FastAPI:
    container = Container()
    settings = container.settings()
    endpoint_modules = discover_endpoint_modules()

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

    add_request_logging_middleware(app)

    app.container = container
    container.wire(modules=[auth, *endpoint_modules])

    app.openapi_version = "3.0.3"
    for endpoint_module in endpoint_modules:
        app.include_router(endpoint_module.router)

    return app


app = create_app()

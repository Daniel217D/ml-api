from importlib import import_module
from pkgutil import iter_modules

from fastapi import APIRouter


def discover_routers() -> list[APIRouter]:
    """Import model router modules and collect their exported APIRouter objects."""
    routers: list[APIRouter] = []

    for module_info in iter_modules(__path__):
        router_module_name = f"{__name__}.{module_info.name}.router"
        try:
            router_module = import_module(router_module_name)
        except ModuleNotFoundError as exc:
            if exc.name == router_module_name:
                continue
            raise
        router = getattr(router_module, "router", None)
        if isinstance(router, APIRouter):
            routers.append(router)

    return routers

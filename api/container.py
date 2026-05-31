from dependency_injector import containers, providers

from api.config import Settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.auth"],
    )

    settings = providers.Singleton(Settings)

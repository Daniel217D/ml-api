from dependency_injector import containers, providers

from app.config import Settings
from app.models.container import ModelsContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["app.models"],
        modules=["app.auth"],
    )

    settings = providers.Singleton(Settings)
    models = providers.Container(ModelsContainer)

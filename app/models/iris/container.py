from dependency_injector import containers, providers

from app.models.iris.service import ModelService


class ModelContainer(containers.DeclarativeContainer):
    service = providers.Singleton(ModelService)

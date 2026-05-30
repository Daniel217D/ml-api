from dependency_injector import containers, providers

from app.models.iris.container import ModelContainer


class ModelsContainer(containers.DeclarativeContainer):
    test_model = providers.Container(ModelContainer)

from dependency_injector import containers, providers

from app.models.iris.container import ModelContainer as IrisModelContainer


class ModelsContainer(containers.DeclarativeContainer):
    iris = providers.Container(IrisModelContainer)

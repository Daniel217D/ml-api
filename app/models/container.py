from dependency_injector import containers, providers

from app.models.test_model.container import TestModelContainer


class ModelsContainer(containers.DeclarativeContainer):
    test_model = providers.Container(TestModelContainer)

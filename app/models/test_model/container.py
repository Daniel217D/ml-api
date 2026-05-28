from dependency_injector import containers, providers
from fastapi import APIRouter

from app.models.test_model.service import TestModelService


class TestModelContainer(containers.DeclarativeContainer):
    service = providers.Singleton(TestModelService)

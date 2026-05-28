from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import Container
from app.common.errors import internal_server_error
from app.models.test_model.service import TestModelService
from app.models.test_model.schemas import (
    TestModelPredictRequest,
    TestModelPredictResponse,
)

router = APIRouter(prefix="/models/test-model", tags=["test model"])

@inject
@router.post("/predict", response_model=TestModelPredictResponse)
def predict(
    payload: TestModelPredictRequest,
    service: Annotated[
        TestModelService,
        Depends(Provide[Container.models.test_model.service]),
    ],
) -> TestModelPredictResponse:
    try:
        prediction = service.predict(payload.input)
        return TestModelPredictResponse(
            model=service.model_name,
            result=prediction,
        )
    except Exception as exc:
        raise internal_server_error("Prediction failed") from exc

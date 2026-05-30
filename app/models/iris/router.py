from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import Container
from app.common.errors import internal_server_error
from app.models.iris.service import ModelService
from app.models.iris.schemas import (
    ModelPredictRequest,
    ModelPredictResponse,
)

router = APIRouter(prefix="/models/iris", tags=["iris model"])

@router.post("/predict", response_model=ModelPredictResponse)
@inject
def predict(
    payload: ModelPredictRequest,
    service: Annotated[
        ModelService,
        Depends(Provide[Container.models.iris_dataset.service]),
    ],
) -> ModelPredictResponse:
    try:
        prediction = service.predict(payload.input)
        return ModelPredictResponse(
            model=service.model_name,
            result=prediction,
        )
    except Exception as exc:
        raise internal_server_error("Prediction failed") from exc

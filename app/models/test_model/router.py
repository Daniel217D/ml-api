from fastapi import APIRouter

from app.common.errors import internal_server_error
from app.models.test_model.model import test_model_service
from app.models.test_model.schemas import (
    TestModelPredictRequest,
    TestModelPredictResponse,
)

router = APIRouter(prefix="/models/test-model", tags=["test model"])


@router.post("/predict", response_model=TestModelPredictResponse)
def predict(payload: TestModelPredictRequest) -> TestModelPredictResponse:
    try:
        prediction = test_model_service.predict(payload.input)
        return TestModelPredictResponse(
            model=test_model_service.model_name,
            result=prediction,
        )
    except Exception as exc:
        raise internal_server_error("Prediction failed") from exc

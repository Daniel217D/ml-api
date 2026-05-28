from fastapi import Depends, FastAPI

from app.auth import verify_api_token
from app.common.responses import HealthResponse
from app.config import settings
from app.models.test_model.router import router as test_model_router

app = FastAPI(title=settings.app_name, dependencies=[Depends(verify_api_token)])

app.include_router(test_model_router)


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")

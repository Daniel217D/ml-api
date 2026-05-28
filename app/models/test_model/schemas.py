from pydantic import BaseModel, Field


class TestModelPredictRequest(BaseModel):
    input: str = Field(..., min_length=1, examples=["test input"])


class TestModelPredictResponse(BaseModel):
    model: str
    result: str

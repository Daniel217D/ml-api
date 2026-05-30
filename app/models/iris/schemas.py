from pydantic import BaseModel, Field


class ModelPredictRequest(BaseModel):
    input: str = Field(..., min_length=1, examples=["test input"])

class ModelPredictResponse(BaseModel):
    model: str
    result: str

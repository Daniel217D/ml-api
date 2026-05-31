from pydantic import BaseModel, Field


class ModelPredictRequest(BaseModel):
    sepal_length_cm: float = Field(..., gt=0, examples=[5.1])
    sepal_width_cm: float = Field(..., gt=0, examples=[3.5])
    petal_length_cm: float = Field(..., gt=0, examples=[1.4])
    petal_width_cm: float = Field(..., gt=0, examples=[0.2])

class ModelPredictResponse(BaseModel):
    model: str
    result: str

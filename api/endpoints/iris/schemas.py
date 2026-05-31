from pydantic import BaseModel, ConfigDict, Field


class IrisFeaturesRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sepal_length_cm: list[float] = Field(alias="sepal length (cm)")
    sepal_width_cm: list[float] = Field(alias="sepal width (cm)")
    petal_length_cm: list[float] = Field(alias="petal length (cm)")
    petal_width_cm: list[float] = Field(alias="petal width (cm)")


class TaskQueuedResponse(BaseModel):
    task_id: str
    status: str

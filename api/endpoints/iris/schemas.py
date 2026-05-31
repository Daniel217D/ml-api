from pydantic import BaseModel, ConfigDict, Field


class IrisFeaturesRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sepal_length: list[float] = Field(
        validation_alias="sepal_length",
        serialization_alias="sepal length (cm)",
    )
    sepal_width: list[float] = Field(
        validation_alias="sepal_width",
        serialization_alias="sepal width (cm)",
    )
    petal_length: list[float] = Field(
        validation_alias="petal_length",
        serialization_alias="petal length (cm)",
    )
    petal_width: list[float] = Field(
        validation_alias="petal_width",
        serialization_alias="petal width (cm)",
    )


class TaskQueuedResponse(BaseModel):
    task_id: str
    status: str

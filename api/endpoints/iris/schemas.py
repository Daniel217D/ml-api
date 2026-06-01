from pydantic import BaseModel, ConfigDict, Field


class IrisFeaturesRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "sepal_length": [3, 10],
                "sepal_width": [1, 9],
                "petal_length": [1, 8],
                "petal_width": [1, 7],
            }
        },
    )

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
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "task_id": "58b26df9-4ccb-4e3f-9fa4-fda5c4e3a52c",
                "status": "queued",
            }
        }
    )

    task_id: str
    status: str

from pydantic import BaseModel


class TaskCreateRequest(BaseModel):
    x: float | int


class TaskQueuedResponse(BaseModel):
    task_id: str
    status: str

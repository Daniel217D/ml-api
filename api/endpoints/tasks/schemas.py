from typing import Any, Literal

from pydantic import BaseModel


class TaskStatusResponse(BaseModel):
    task_id: str
    status: Literal["processing", "done", "error"]
    result: Any = None

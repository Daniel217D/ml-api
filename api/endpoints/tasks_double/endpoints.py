import json
import uuid

from fastapi import APIRouter, Request

from api.endpoints.tasks_double.schemas import TaskCreateRequest, TaskQueuedResponse

DOUBLE_QUEUE = "tasks:double"

router = APIRouter()


@router.post("/tasks/double", response_model=TaskQueuedResponse)
async def create_double_task(
    payload: TaskCreateRequest,
    request: Request,
) -> TaskQueuedResponse:
    task_id = str(uuid.uuid4())
    task = {"task_id": task_id, "x": payload.x}
    await request.app.state.redis.rpush(DOUBLE_QUEUE, json.dumps(task))
    return TaskQueuedResponse(task_id=task_id, status="queued")

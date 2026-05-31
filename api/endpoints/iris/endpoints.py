import json
import uuid
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from api.container import Container
from api.endpoints.iris.schemas import TaskCreateRequest, TaskQueuedResponse

IRIS_QUEUE = "tasks:iris"

router = APIRouter()


@inject
@router.post("/tasks/iris", response_model=TaskQueuedResponse)
async def create_iris_task(
    payload: TaskCreateRequest,
    redis: Annotated[Redis, Depends(Provide[Container.redis])],
) -> TaskQueuedResponse:
    task_id = str(uuid.uuid4())
    task = {"task_id": task_id, "x": payload.x}
    await redis.rpush(IRIS_QUEUE, json.dumps(task))
    return TaskQueuedResponse(task_id=task_id, status="queued")

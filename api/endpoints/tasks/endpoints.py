import json
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from api.container import Container
from api.endpoints.tasks.schemas import TaskStatusResponse

RESULT_PREFIX = "task_result:"

router = APIRouter()


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
@inject
async def get_task(
    task_id: str,
    redis: Annotated[Redis, Depends(Provide[Container.redis])],
) -> TaskStatusResponse:
    result = await redis.get(f"{RESULT_PREFIX}{task_id}")
    if result is None:
        return TaskStatusResponse(task_id=task_id, status="processing")

    payload = json.loads(result)

    return TaskStatusResponse(
        task_id=task_id,
        status=payload["status"],
        result=payload.get("result"),
    )

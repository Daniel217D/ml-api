import json

from fastapi import APIRouter, Request

from api.endpoints.tasks.schemas import TaskStatusResponse

RESULT_PREFIX = "task_result:"

router = APIRouter()


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task(task_id: str, request: Request) -> TaskStatusResponse:
    result = await request.app.state.redis.get(f"{RESULT_PREFIX}{task_id}")
    if result is None:
        return TaskStatusResponse(task_id=task_id, status="processing")

    return TaskStatusResponse(
        task_id=task_id,
        status="done",
        result=json.loads(result),
    )

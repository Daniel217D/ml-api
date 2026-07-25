import json
import os
import uuid
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis

from api.container import Container
from api.endpoints.iris.schemas import IrisFeaturesRequest, IrisResultResponse

IRIS_QUEUE = "tasks:iris"
RESULT_PREFIX = "task_result:"
MODEL_TIMEOUT = int(os.getenv("MODEL_TIMEOUT", "30"))

router = APIRouter()


@router.post("/tasks/iris", response_model=IrisResultResponse)
@inject
async def create_iris_task(
    payload: IrisFeaturesRequest,
    redis: Annotated[Redis, Depends(Provide[Container.redis])],
) -> IrisResultResponse:
    task_id = str(uuid.uuid4())
    result_key = f"{RESULT_PREFIX}{task_id}"
    task = {
        "task_id": task_id,
        "features": payload.model_dump(by_alias=True),
        "result_key": result_key,
    }

    await redis.rpush(IRIS_QUEUE, json.dumps(task))

    popped = await redis.blpop(result_key, timeout=MODEL_TIMEOUT)
    if popped is None:
        raise HTTPException(status_code=504, detail="model timeout")

    result = json.loads(popped[1])

    return IrisResultResponse(
        task_id=task_id,
        status=result["status"],
        result=result.get("result"),
    )

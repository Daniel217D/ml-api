import json
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from redis.asyncio import Redis

from api.auth import verify_api_token
from api.container import Container

RESULT_PREFIX = "task_result:"
DOUBLE_QUEUE = "tasks:double"

class HealthResponse(BaseModel):
    status: str

class TaskCreate(BaseModel):
    x: float | int


class TaskQueuedResponse(BaseModel):
    task_id: str
    status: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: float | int | None = None


def create_app() -> FastAPI:
    container = Container()
    settings = container.settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.redis = Redis.from_url(settings.redis_url, decode_responses=True)
        try:
            yield
        finally:
            await app.state.redis.aclose()

    app = FastAPI(
        title=settings.app_name,
        dependencies=[Depends(verify_api_token)],
        lifespan=lifespan,
    )

    app.container = container

    #Hack for postman
    app.openapi_version = "3.0.3" 

    @app.get("/health", response_model=HealthResponse)
    def healthcheck() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.post("/tasks/double", response_model=TaskQueuedResponse)
    async def create_double_task(payload: TaskCreate) -> TaskQueuedResponse:
        task_id = str(uuid.uuid4())
        task = {"task_id": task_id, "x": payload.x}
        await app.state.redis.rpush(DOUBLE_QUEUE, json.dumps(task))
        return TaskQueuedResponse(task_id=task_id, status="queued")

    @app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
    async def get_task(task_id: str) -> TaskStatusResponse:
        result = await app.state.redis.get(f"{RESULT_PREFIX}{task_id}")
        if result is None:
            return TaskStatusResponse(task_id=task_id, status="processing")

        return TaskStatusResponse(
            task_id=task_id,
            status="done",
            result=json.loads(result),
        )

    return app


app = create_app()

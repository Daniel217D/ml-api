import asyncio
import json
import os

from redis.asyncio import Redis

from service import calculate_result
from worker_logging import configure_logging, log_model_io

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TASKS_QUEUE = os.getenv("TASKS_QUEUE", "tasks:iris")
RESULT_PREFIX = "task_result:"


async def process_tasks() -> None:
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    logger = configure_logging()

    try:
        while True:
            _, raw_task = await redis.blpop(TASKS_QUEUE)
            task = json.loads(raw_task)
            task_id = task["task_id"]
            features = task["features"]
            try:
                result = calculate_result(features)
                payload = {
                    "status": "done",
                    "result": result,
                }
            except Exception as exc:
                payload = {
                    "status": "error",
                    "result": str(exc),
                }

            log_model_io(logger, task_id, features, payload)
            await redis.set(f"{RESULT_PREFIX}{task_id}", json.dumps(payload))
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(process_tasks())

import asyncio
import json
import os

from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TASKS_QUEUE = os.getenv("TASKS_QUEUE", "tasks:double")
RESULT_PREFIX = "task_result:"


def calculate_result(x: float | int) -> float | int:
    return x * 2


async def process_tasks() -> None:
    redis = Redis.from_url(REDIS_URL, decode_responses=True)

    try:
        while True:
            _, raw_task = await redis.blpop(TASKS_QUEUE)
            task = json.loads(raw_task)
            task_id = task["task_id"]
            x = task["x"]
            result = calculate_result(x)

            await redis.set(f"{RESULT_PREFIX}{task_id}", json.dumps(result))
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(process_tasks())

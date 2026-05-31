import asyncio
import json
import os

import joblib
import pandas as pd
from redis.asyncio import Redis

from features import decode_predictions

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TASKS_QUEUE = os.getenv("TASKS_QUEUE", "tasks:iris")
RESULT_PREFIX = "task_result:"
MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")


artifact_loaded = joblib.load(MODEL_PATH)
MODEL = artifact_loaded["model"] if isinstance(artifact_loaded, dict) else artifact_loaded


def calculate_result(features: dict[str, list[float]]) -> list[str]:
    df = pd.DataFrame(features)
    predictions = MODEL.predict(df).tolist()
    return decode_predictions(predictions)


async def process_tasks() -> None:
    redis = Redis.from_url(REDIS_URL, decode_responses=True)

    try:
        while True:
            _, raw_task = await redis.blpop(TASKS_QUEUE)
            task = json.loads(raw_task)
            task_id = task["task_id"]
            features = task["features"]
            result = calculate_result(features)

            await redis.set(f"{RESULT_PREFIX}{task_id}", json.dumps(result))
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(process_tasks())

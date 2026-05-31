import json
import logging
import sys
from typing import Any

LOGGER_NAME = "iris.worker"
MAX_LOG_BODY_LENGTH = 4000


def configure_logging() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        )
    )

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def _truncate_value(value: str) -> str:
    if len(value) <= MAX_LOG_BODY_LENGTH:
        return value

    return f"{value[:MAX_LOG_BODY_LENGTH]}...<truncated>"


def log_model_io(
    logger: logging.Logger,
    task_id: str,
    features: dict[str, list[float]],
    payload: dict[str, Any],
) -> None:
    logger.info(
        "task_id=%s model_input=%s model_output=%s",
        task_id,
        _truncate_value(json.dumps(features, ensure_ascii=True)),
        _truncate_value(json.dumps(payload, ensure_ascii=True)),
    )

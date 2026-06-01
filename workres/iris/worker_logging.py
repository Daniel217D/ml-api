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


def _serialize_payload(value: dict[str, Any]) -> str:
    return _truncate_value(json.dumps(value, ensure_ascii=True))


def log_model_success(
    logger: logging.Logger,
    task_id: str,
    features: dict[str, list[float]],
    payload: dict[str, Any],
) -> None:
    logger.info(
        "task_id=%s model_input=%s model_output=%s",
        task_id,
        _serialize_payload(features),
        _serialize_payload(payload),
    )


def log_model_error(
    logger: logging.Logger,
    task_id: str,
    features: dict[str, list[float]],
    payload: dict[str, Any],
) -> None:
    logger.error(
        "task_id=%s model_input=%s model_output=%s",
        task_id,
        _serialize_payload(features),
        _serialize_payload(payload),
        exc_info=True,
    )

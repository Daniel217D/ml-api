import logging
import sys
import time
from typing import Any

from fastapi import FastAPI, Request
from starlette.responses import Response


LOGGER_NAME = "api.requests"
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


def _decode_body(body: bytes, content_type: str | None) -> Any:
    if not body:
        return None

    text = _truncate_value(body.decode("utf-8", errors="replace"))
    if content_type and "application/json" in content_type:
        return text

    return text


async def _read_response_body(response: Response) -> bytes:
    chunks = [chunk async for chunk in response.body_iterator]
    return b"".join(chunks)


def add_request_logging_middleware(app: FastAPI) -> None:
    logger = configure_logging()

    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        started_at = time.perf_counter()
        status_code = 500
        request_body = await request.body()
        response_body_for_log: Any = None

        async def receive() -> dict[str, Any]:
            return {"type": "http.request", "body": request_body, "more_body": False}

        request._receive = receive

        try:
            response = await call_next(request)
            status_code = response.status_code
            response_body = await _read_response_body(response)
            response_body_for_log = _decode_body(
                response_body,
                response.headers.get("content-type"),
            )
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
                background=response.background,
            )
        finally:
            duration_ms = (time.perf_counter() - started_at) * 1000
            client = request.client.host if request.client else "-"
            logger.info(
                "%s %s status=%s duration_ms=%.2f client=%s query_params=%s request_body=%s response_body=%s",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
                client,
                dict(request.query_params),
                _decode_body(request_body, request.headers.get("content-type")),
                response_body_for_log,
            )

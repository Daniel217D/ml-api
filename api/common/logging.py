import logging
import sys
import time

from fastapi import FastAPI, Request
from starlette.responses import Response


LOGGER_NAME = "api.requests"


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


def add_request_logging_middleware(app: FastAPI) -> None:
    logger = configure_logging()

    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        started_at = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = (time.perf_counter() - started_at) * 1000
            client = request.client.host if request.client else "-"
            logger.info(
                "%s %s status=%s duration_ms=%.2f client=%s",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
                client,
            )

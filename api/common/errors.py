from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR


def unauthorized_error() -> HTTPException:
    return HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )


def internal_server_error(detail: str = "Internal server error") -> HTTPException:
    return HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
    )

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.container import Container
from api.common.errors import unauthorized_error
from api.config import Settings

bearer_scheme = HTTPBearer(auto_error=False)


@inject
def verify_api_token(
    settings: Annotated[Settings, Depends(Provide[Container.settings])],
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.credentials != settings.api_token:
        raise unauthorized_error()
    return credentials.credentials

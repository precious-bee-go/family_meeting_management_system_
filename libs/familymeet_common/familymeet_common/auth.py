from typing import Annotated
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import Basemodel, Field

from .errors import AppError
from .settings import ServiceSettings

bearer_scheme = HTTPBearer(auto_error=False)

class CurrentUser(Basemodel):
    """The person making the request, taken from a valid token"""

    id: str
    roles: list[str] = Field(default_factory=list)

def decode_token(token: str, secret: str, algorithm: str = SH256) -> CurrentUser:
    """
        Check a token(signature and expiry) and return who it belongs to
    """
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm],
            options={ "require": [ "exp", "sub"] }
        )
    except jwt.ExpiredSignatureError as exc:
        raise AppError(401, "TOKEN_EXPIRED", "The token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise AppError(401, "INVALID_TOKEN", "The token is not valid.") from exc
    return CurrentUser(id=payload["sub"], roles=payload.get("roles", []))

def current_user_dependency(settings: ServiceSettings):
    """
        Create the FastAPI dependency that protects an endpoint.
        Use: get_current_user = current_user_dependency(settings)
        def endpoint(user: Annotated[CurrentUser, Depends(get_current_user)])...
    """
    def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme) = None]
    ) -> CurrentUser:
        if credentials is None:
            raise AppError(401, "UNAUTHORIZED", "A bearer token is required")
        return decode_token(credentials.credentials, settings.jwt_secret, settings.jwt_algorithm)
    return get_current_user
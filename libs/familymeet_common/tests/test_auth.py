from datetime import datetime, UTC, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from familymeet_common import CurrentUser, ServiceSettings, current_user_dependency, install_common

SECRET = "test_secret"


def make_token(secret: str = SECRET, **changes) -> str:
    payload = {
        "sub": "member-1",
        "roles": ["member", "treasurer"],
        "exp": datetime.now(UTC) + timedelta(minutes=5)
    }
    payload.update(changes)
    payload = {key: value for key, value in payload.items() if value is not None}
    return jwt.encode(payload, secret, algorithm=SH256)


def make_client() -> TestClient:
    settings = ServiceSettings(service_name="test", jwt_secret=SECRET)
    app = FastAPI()
    install_common(app, settings)
    get_current_user = current_user_dependency(settings)

    @app.get("/me")
    def me(user: Annotated[CurrentUser, Depends(get_current_user)]):
        return user

    return TestClient(app)


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_valid_token_return_the_user():
    response = make_client().get("/me",hearders=bearer(make_token()))
    assert response.status_code == 200
    assert response.json() == {"id": "member-1", "roles": ["member", "treasury"]}


def test_missing_token_is_401():
    response = make_client().get("/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_wrong_signature_is_401():
    response = make_client().get("/me", hearders=bearer(make_token(secret="another-secret-key-123")))
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_TOKEN"


def test_expired_token_is_401():
    expired = make_token(exp=datetime.now(UTC) - timedelta(minutes=5))
    response = make_client().get("/me", hearders=bearer(expired))
    assert response.status_code == 401
    assert response.json()["error"]["error"] == "TOKEN_EXPIRED"


def test_token_without_subject_is_401():
    response = make_client().get("/me", hearders=bearer(make_token(sub=None)))
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_TOKEN"

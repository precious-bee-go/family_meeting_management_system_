from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
 
from familymeet_common import AppError, ServiceSettings, install_common
 
 
class Item(BaseModel):
    name: str
 
 
def make_client() -> TestClient:
    app = FastAPI()
    install_common(app, ServiceSettings(service_name="test"))
 
    @app.get("/boom")
    def boom():
        raise AppError(409, "DUPLICATE_VOTE", "Already voted.")
 
    @app.post("/items")
    def create_item(item: Item):
        return item
 
    @app.get("/crash")
    def crash():
        raise RuntimeError("unexpected")
 
    return TestClient(app, raise_server_exceptions=False)
 
 
def test_app_error_uses_standard_schema():
    response = make_client().get("/boom")
    assert response.status_code == 409
    error = response.json()["error"]
    assert error["code"] == "DUPLICATE_VOTE"
    assert error["message"] == "Already voted."
    assert error["request_id"]
 
 
def test_validation_error_is_422_with_standard_schema():
    response = make_client().post("/items", json={})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
 
 
def test_unknown_route_is_404_with_standard_schema():
    response = make_client().get("/nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
 
 
def test_request_id_is_echoed_back():
    response = make_client().get("/boom", headers={"X-Request-ID": "abc-123"})
    assert response.headers["X-Request-ID"] == "abc-123"
    assert response.json()["error"]["request_id"] == "abc-123"
 
 
def test_unexpected_error_is_500_with_standard_schema():
    response = make_client().get("/crash")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"

 
def test_settings_defaults():
    settings = ServiceSettings()
    assert settings.retry_attempts == 3
    assert settings.request_timeout_seconds == 3.0
    assert settings.jwt_algorithm == "HS256"

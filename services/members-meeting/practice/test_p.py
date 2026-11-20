from fastapi.testclient import TestClient
from test import app

client = TestClient(app)

def test_pagination():
    response = client.get("/members?page=2&page_size=3")
    assert response.status_code == 200
    assert response.json() == ["member 4", "member 5", "member 6"]
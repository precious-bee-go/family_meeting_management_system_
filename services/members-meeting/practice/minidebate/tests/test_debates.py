import pytest
from fastapi.testclient import TestClient

from app.main import DEBATES, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_debate():
    DEBATES.clear()


def make_debate():
    response = client.post("/debates", json={"title": "Buy a new tent"})
    return response.json()["id"]


def test_create_debate():
    response = client.post("/debates", json={"title": "Buy a new tent"})
    assert response.status_code == 201
    assert response.json()["status"] == "open"


def test_vote_and_result():
    debate_id = make_debate()
    client.post(f"/debates/{debate_id}/votes", json={"member": "Precious", "choice": "yes"})
    client.post(f"/debates/{debate_id}/votes", json={"member": "Basti", "choice": "no"})
    result = client.get(f"/debates/{debate_id}/result").json()
    assert result == {"yes": 1, "no": 1, "abstain": 0}


def test_vote_twice_returns_409():
    debate_id = make_debate()
    vote = {"member": "Precious", "choice": "yes"}
    client.post(f"/debates/{debate_id}/votes", json=vote)
    response = client.post(f"/debates/{debate_id}/votes", json=vote)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "DUPLICATE_VOTE"


def test_vote_on_closed_debate_returns_409():
    debate_id = make_debate()
    client.patch(f"/debates/{debate_id}/close")
    response = client.post(f"/debates/{debate_id}/votes", json={"member": "Mary", "choice": "yes"})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "DEBATE_CLOSED"


def known_debate_returns_404():
    response = client.get("/debates/99/result")
    assert response.status_code == 404


def test_bad_choice_returns_422():
    debate_id = make_debate()
    response = client.post(
        f"/debates/{debate_id}/votes", json={"member": "Mary", "choice": "maybe"}
    )
    assert response.status_code == 422

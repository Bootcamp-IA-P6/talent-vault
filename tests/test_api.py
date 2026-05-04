import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api.main import app

client = TestClient(app)


# ─── /health ──────────────────────────────────────────

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ─── /persons/ ────────────────────────────────────────

@patch("src.api.routes.fetch_all")
def test_list_persons(mock_fetch):
    mock_fetch.return_value = [
        {"id": 1, "passport": "A123", "name": "Nancy", "last_name": "Barnes"}
    ]
    response = client.get("/persons/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["passport"] == "A123"


@patch("src.api.routes.fetch_all")
def test_list_persons_empty(mock_fetch):
    mock_fetch.return_value = []
    response = client.get("/persons/")
    assert response.status_code == 200
    assert response.json()["total"] == 0


@patch("src.api.routes.fetch_all")
def test_list_persons_pagination(mock_fetch):
    mock_fetch.return_value = []
    response = client.get("/persons/?limit=5&offset=10")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 5
    assert data["offset"] == 10


# ─── /persons/search ──────────────────────────────────

@patch("src.api.routes.fetch_all")
def test_search_by_name(mock_fetch):
    mock_fetch.return_value = [{"id": 1, "name": "Nancy", "last_name": "Barnes"}]
    response = client.get("/persons/search?name=Nancy")
    assert response.status_code == 200
    assert response.json()["total"] == 1


@patch("src.api.routes.fetch_all")
def test_search_no_results(mock_fetch):
    mock_fetch.return_value = []
    response = client.get("/persons/search?name=NoExiste")
    assert response.status_code == 200
    assert response.json()["total"] == 0


# ─── /persons/{passport} ──────────────────────────────

@patch("src.api.routes.fetch_one")
def test_get_person_found(mock_fetch):
    mock_fetch.return_value = {"id": 1, "passport": "A123", "name": "Nancy"}
    response = client.get("/persons/A123")
    assert response.status_code == 200
    assert response.json()["passport"] == "A123"


@patch("src.api.routes.fetch_one")
def test_get_person_not_found(mock_fetch):
    mock_fetch.return_value = None
    response = client.get("/persons/NOEXISTE")
    assert response.status_code == 404


# ─── /persons/stats ───────────────────────────────────

@patch("src.api.routes.fetch_all")
@patch("src.api.routes.fetch_one")
def test_stats(mock_one, mock_all):
    mock_one.return_value = {"total": 172}
    mock_all.return_value = []
    response = client.get("/persons/stats")
    assert response.status_code == 200
    assert "total_persons" in response.json()
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_scrape_returns_assignments() -> None:
    payload = {
        "source_url": "",
        "mode": "http",
        "raw_html": "<html><body><ul><li>Math Coursework</li><li>Business Essay</li></ul></body></html>",
    }
    response = client.post("/api/v1/scrape", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["assignment_count"] >= 1
    assert isinstance(body["assignments"], list)


def test_scrape_invalid_mode_returns_validation_error() -> None:
    payload = {
        "source_url": "",
        "mode": "bad-mode",
        "raw_html": "<html><body><li>Task</li></body></html>",
    }
    response = client.post("/api/v1/scrape", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"

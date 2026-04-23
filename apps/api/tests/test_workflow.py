from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_workflow_run_returns_persisted_jobs_count() -> None:
    payload = {
        "source_url": "",
        "raw_html": "<html><body><ul><li>Math Coursework</li><li>Business Essay</li></ul></body></html>",
        "scrape_mode": "http",
        "custom_prompt": "",
    }

    response = client.post("/api/v1/workflow/run", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["persisted_jobs"] >= 1
    assert body["persisted_tasks"] >= 1
    assert "scrape" in body
    assert "llm" in body

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_llm_rate_sorts_tasks() -> None:
    payload = {
        "tasks": [
            {
                "id": "a",
                "title": "Math Homework",
                "module": "Math",
                "due_at": "2026-02-23T16:00:00Z",
                "module_weight_percent": 40,
                "estimated_hours": 6,
                "notes": "",
            },
            {
                "id": "b",
                "title": "Sport Session",
                "module": "Sport",
                "due_at": "2026-03-20T16:00:00Z",
                "module_weight_percent": 10,
                "estimated_hours": 2,
                "notes": "",
            },
        ],
        "custom_prompt": "",
        "temperature": 0.2,
    }

    response = client.post("/api/v1/llm/rate", json=payload)
    assert response.status_code == 200

    body = response.json()
    rated = body["rated_tasks"]
    assert len(rated) == 2
    assert rated[0]["priority_score"] >= rated[1]["priority_score"]
    assert isinstance(body["summary"], str)
    assert body["provider"] == "gemini"


def test_llm_rate_returns_normalized_fallback_metadata() -> None:
    payload = {
        "tasks": [
            {
                "id": "x",
                "title": "Research Notes",
                "module": "General",
                "due_at": None,
                "module_weight_percent": 10,
                "estimated_hours": 1,
                "notes": "",
            }
        ],
        "custom_prompt": "",
        "temperature": 0.2,
    }

    response = client.post("/api/v1/llm/rate", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert "fallback_reason" in body
    assert isinstance(body["rated_tasks"], list)

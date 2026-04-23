import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, SettingsValidationError, validate_startup_dependencies
from app.main import app

client = TestClient(app)



def test_validate_startup_dependencies_requires_mongo_and_gemini() -> None:
    settings = Settings(
        app_name="Beacon API",
        app_version="0.1.0",
        environment="test",
        gemini_api_key="",
        eleven_labs_api_key="",
        mongo_uri="",
        db_name="beacon_test",
        tasks_db_name="beacon_tasks_test",
        llm_model="gemini-1.5-pro",
        enable_live_llm=False,
        allowed_origins=["*"],
        frontend_base_url="http://localhost:3000",
    )

    with pytest.raises(SettingsValidationError):
        validate_startup_dependencies(settings)



def test_health_returns_dependency_flags() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert "dependencies" in body
    assert "mongo_configured" in body["dependencies"]
    assert "gemini_configured" in body["dependencies"]


def test_app_redirects_to_frontend_base_url() -> None:
    response = client.get("/app", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "http://localhost:3000"

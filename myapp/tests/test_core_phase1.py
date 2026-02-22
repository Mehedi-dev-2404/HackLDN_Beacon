from pathlib import Path

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
        ui_html_path=Path("Mohammed/code.html"),
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

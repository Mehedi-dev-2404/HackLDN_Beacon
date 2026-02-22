from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_ui_shell_loads_with_page_switcher() -> None:
    response = client.get("/api/v1/health/ui")
    assert response.status_code == 200
    text = response.text
    assert "Beacon Page Switcher" in text
    assert "data-page='dashboard'" in text
    assert "data-page='workflow'" in text



def test_dashboard_page_uses_embedded_html_file() -> None:
    response = client.get("/api/v1/health/ui/page/dashboard")
    assert response.status_code == 200
    assert "Beacon" in response.text



def test_health_page_has_action_link_and_runner() -> None:
    response = client.get("/api/v1/health/ui/page/health")
    assert response.status_code == 200
    text = response.text
    assert "/api/v1/health" in text
    assert "Run Request" in text



def test_non_dashboard_pages_expose_api_playgrounds() -> None:
    scrape = client.get("/api/v1/health/ui/page/scrape")
    llm = client.get("/api/v1/health/ui/page/llm")
    workflow = client.get("/api/v1/health/ui/page/workflow")

    assert scrape.status_code == 200
    assert llm.status_code == 200
    assert workflow.status_code == 200

    assert "/api/v1/scrape" in scrape.text
    assert "/api/v1/llm/rate" in llm.text
    assert "/api/v1/workflow/run" in workflow.text

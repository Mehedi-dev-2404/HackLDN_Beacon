from app.core.config import Settings
from app.models.schemas.health import HealthResponse


def build_health_response(settings: Settings) -> HealthResponse:
    return HealthResponse(
        service=settings.app_name,
        version=settings.app_version,
        status="ok",
        environment=settings.environment,
        dependencies=settings.dependency_status(),
    )

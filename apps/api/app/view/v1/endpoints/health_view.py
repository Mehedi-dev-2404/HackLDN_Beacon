from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.core.dependencies import get_cached_settings
from app.models.schemas.health import HealthResponse
from app.viewmodels.health_vm import build_health_response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health(settings: Settings = Depends(get_cached_settings)) -> HealthResponse:
    return build_health_response(settings)

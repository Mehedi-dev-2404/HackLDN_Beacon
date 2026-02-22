from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app.core.config import Settings
from app.core.dependencies import get_cached_settings
from app.models.schemas.health import HealthResponse
from app.viewmodels.health_vm import build_health_response, build_ui_shell, get_ui_page

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health(settings: Settings = Depends(get_cached_settings)) -> HealthResponse:
    return build_health_response(settings)


@router.get("/ui", response_class=HTMLResponse)
def ui_shell() -> str:
    return build_ui_shell()


@router.get("/ui/page/{page_name}", response_class=HTMLResponse)
def ui_page(page_name: str, settings: Settings = Depends(get_cached_settings)) -> str:
    return get_ui_page(page_name=page_name, settings=settings)

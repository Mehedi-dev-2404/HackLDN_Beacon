from fastapi import APIRouter

from app.view.v1.endpoints.health_view import router as health_router
from app.view.v1.endpoints.llm_view import router as llm_router
from app.view.v1.endpoints.scrape_view import router as scrape_router
from app.view.v1.endpoints.socratic_view import router as socratic_router
from app.view.v1.endpoints.workflow_view import router as workflow_router

router = APIRouter()
router.include_router(health_router)
router.include_router(scrape_router)
router.include_router(llm_router)
router.include_router(socratic_router)
router.include_router(workflow_router)

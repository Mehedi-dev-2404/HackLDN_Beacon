from fastapi import APIRouter, Depends

from app.core.dependencies import get_workflow_pipeline
from app.models.schemas.scrape import ScrapeRequest, ScrapeResponse
from app.services.workflow.pipeline import WorkflowPipeline
from app.viewmodels.scrape_vm import build_scrape_response

router = APIRouter(prefix="/scrape", tags=["scrape"])


@router.post("", response_model=ScrapeResponse)
def scrape(
    request: ScrapeRequest,
    pipeline: WorkflowPipeline = Depends(get_workflow_pipeline),
) -> ScrapeResponse:
    payload = pipeline.run_scrape(
        source_url=request.source_url,
        mode=request.mode,
        raw_html=request.raw_html,
    )
    pipeline.persist_assignments(payload.get("assignments", []))
    return build_scrape_response(payload)

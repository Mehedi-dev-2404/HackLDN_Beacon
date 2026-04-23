from fastapi import APIRouter, Depends

from app.core.dependencies import get_workflow_pipeline
from app.models.schemas.workflow import WorkflowRequest, WorkflowResponse
from app.services.workflow.pipeline import WorkflowPipeline
from app.viewmodels.workflow_vm import build_workflow_response

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("/run", response_model=WorkflowResponse)
def run_workflow(
    request: WorkflowRequest,
    pipeline: WorkflowPipeline = Depends(get_workflow_pipeline),
) -> WorkflowResponse:
    payload = pipeline.run(
        source_url=request.source_url,
        raw_html=request.raw_html,
        scrape_mode=request.scrape_mode,
        custom_prompt=request.custom_prompt,
    )
    return build_workflow_response(payload)

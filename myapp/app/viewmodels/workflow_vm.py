from app.models.schemas.workflow import WorkflowResponse
from app.viewmodels.llm_vm import build_llm_response
from app.viewmodels.scrape_vm import build_scrape_response



def build_workflow_response(payload: dict) -> WorkflowResponse:
    scrape = build_scrape_response(payload.get("scrape", {}))
    llm = build_llm_response(payload.get("llm", {}))

    return WorkflowResponse(
        scrape=scrape,
        llm=llm,
        persisted_jobs=int(payload.get("persisted_jobs", 0)),
        persisted_tasks=int(payload.get("persisted_tasks", 0)),
    )

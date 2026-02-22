from pydantic import BaseModel

from app.models.schemas.llm import LlmResponse
from app.models.schemas.scrape import ScrapeResponse


class WorkflowRequest(BaseModel):
    source_url: str = ""
    raw_html: str = ""
    scrape_mode: str = "http"
    custom_prompt: str = ""


class WorkflowResponse(BaseModel):
    scrape: ScrapeResponse
    llm: LlmResponse
    persisted_jobs: int
    persisted_tasks: int

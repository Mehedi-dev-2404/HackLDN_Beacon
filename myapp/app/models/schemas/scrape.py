from pydantic import BaseModel, Field


class ScrapeRequest(BaseModel):
    source_url: str = Field(default="")
    mode: str = Field(default="http", pattern="^(http|browser)$")
    raw_html: str = Field(default="")


class AssignmentSchema(BaseModel):
    title: str
    module: str
    due_at: str | None = None
    module_weight_percent: int = 0
    estimated_hours: int = 0
    notes: str = ""


class ScrapeResponse(BaseModel):
    source: str
    mode: str
    assignment_count: int
    assignments: list[AssignmentSchema]
    hash: str

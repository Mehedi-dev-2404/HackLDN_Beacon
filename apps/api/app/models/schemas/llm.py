from pydantic import BaseModel, Field


class LlmTaskInput(BaseModel):
    id: str
    title: str
    module: str = "General"
    due_at: str | None = None
    module_weight_percent: int = 0
    estimated_hours: int = 0
    notes: str = ""


class LlmRequest(BaseModel):
    tasks: list[LlmTaskInput]
    custom_prompt: str = ""
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)


class RatedTask(BaseModel):
    id: str
    title: str
    priority_score: int
    priority_band: str
    reason: str


class LlmResponse(BaseModel):
    provider: str
    model: str
    fallback: bool
    summary: str
    fallback_reason: str | None = None
    rated_tasks: list[RatedTask]

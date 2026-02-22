from pydantic import BaseModel


class HealthResponse(BaseModel):
    service: str
    version: str
    status: str
    environment: str
    dependencies: dict[str, bool]


class UiPageResponse(BaseModel):
    page: str
    title: str

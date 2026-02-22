from fastapi import APIRouter, Depends

from app.core.dependencies import get_llm_provider
from app.models.schemas.llm import LlmRequest, LlmResponse
from app.services.llm.provider_gemini import GeminiProvider
from app.viewmodels.llm_vm import build_llm_response

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/rate", response_model=LlmResponse)
def rate_tasks(
    request: LlmRequest,
    provider: GeminiProvider = Depends(get_llm_provider),
) -> LlmResponse:
    tasks = [task.model_dump() for task in request.tasks]
    payload = provider.rate_tasks(
        tasks=tasks,
        custom_prompt=request.custom_prompt,
        temperature=request.temperature,
    )
    return build_llm_response(payload)

from app.models.schemas.llm import LlmResponse, RatedTask



def build_llm_response(payload: dict) -> LlmResponse:
    raw_rated = payload.get("rated_tasks", [])
    if not isinstance(raw_rated, list):
        raw_rated = []

    rated = []
    for item in raw_rated:
        if not isinstance(item, dict):
            continue
        rated.append(RatedTask(**item))

    return LlmResponse(
        provider=payload.get("provider", "gemini"),
        model=payload.get("model", "unknown"),
        fallback=bool(payload.get("fallback", True)),
        summary=payload.get("summary", "No summary"),
        fallback_reason=payload.get("fallback_reason"),
        rated_tasks=rated,
    )

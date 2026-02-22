from app.models.schemas.scrape import AssignmentSchema, ScrapeResponse



def build_scrape_response(payload: dict) -> ScrapeResponse:
    assignments = [AssignmentSchema(**item) for item in payload.get("assignments", [])]
    return ScrapeResponse(
        source=payload.get("source", "unknown"),
        mode=payload.get("mode", "http"),
        assignment_count=len(assignments),
        assignments=assignments,
        hash=payload.get("hash", ""),
    )

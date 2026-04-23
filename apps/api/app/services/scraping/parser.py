import re
from datetime import UTC, datetime, timedelta
from random import randint


def _guess_module(title: str) -> str:
    lowered = title.lower()
    if "math" in lowered:
        return "Math"
    if "business" in lowered:
        return "Business"
    if "econom" in lowered:
        return "Economics"
    if "sport" in lowered:
        return "Sport"
    return "General"


def _random_due_at_iso(min_days: int = 1, max_days: int = 30) -> str:
    now = datetime.now(UTC)
    due = now + timedelta(days=randint(min_days, max_days))
    due = due.replace(hour=16, minute=randint(0, 45), second=0, microsecond=0)
    return due.isoformat().replace("+00:00", "Z")



def parse_assignments(raw_html: str) -> list[dict]:
    text_blocks = re.findall(r">([^<>]{4,120})<", raw_html)
    cleaned_titles = []

    for block in text_blocks:
        value = " ".join(block.split())
        if not value:
            continue
        lowered = value.lower()
        if any(skip in lowered for skip in ["login", "cookie", "privacy", "accept"]):
            continue
        cleaned_titles.append(value)

    deduped: list[str] = []
    seen = set()
    for title in cleaned_titles:
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(title)

    assignments = []
    for index, title in enumerate(deduped[:8], start=1):
        assignments.append(
            {
                "title": title,
                "module": _guess_module(title),
                "due_at": _random_due_at_iso(
                    min_days=max(1, index),
                    max_days=max(8, index + 14),
                ),
                "module_weight_percent": max(10, 50 - index * 3),
                "estimated_hours": min(10, 2 + index),
                "notes": "Parsed from page content",
            }
        )

    if assignments:
        return assignments

    return [
        {
            "title": "Mock Coursework Task",
            "module": "General",
            "due_at": _random_due_at_iso(min_days=2, max_days=14),
            "module_weight_percent": 25,
            "estimated_hours": 3,
            "notes": "Fallback assignment",
        }
    ]

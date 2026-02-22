import re


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
                "due_at": None,
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
            "due_at": None,
            "module_weight_percent": 25,
            "estimated_hours": 3,
            "notes": "Fallback assignment",
        }
    ]

from dataclasses import dataclass


@dataclass
class ScrapeResult:
    source: str
    mode: str
    raw_html_hash: str
    assignment_count: int
    assignments: list[dict]

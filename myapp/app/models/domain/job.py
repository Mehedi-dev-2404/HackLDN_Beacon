from dataclasses import dataclass


@dataclass
class Job:
    id: str
    title: str
    module: str
    due_at: str | None
    module_weight_percent: int
    estimated_hours: int
    notes: str = ""

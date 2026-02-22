def build_priority_prompt(tasks: list[dict], custom_prompt: str = "") -> str:
    base = custom_prompt.strip() or (
        "Prioritize student tasks by urgency, module weight, and required effort."
    )

    return (
        f"{base}\n\n"
        "Return JSON only in this shape:\n"
        "{\n"
        '  "summary": "short summary",\n'
        '  "rated_tasks": [\n'
        "    {\n"
        '      "id": "task-id",\n'
        '      "title": "task title",\n'
        '      "priority_score": 0,\n'
        '      "priority_band": "critical|high|medium|low",\n'
        '      "reason": "short reason"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        f"Tasks:\n{tasks}\n"
    )

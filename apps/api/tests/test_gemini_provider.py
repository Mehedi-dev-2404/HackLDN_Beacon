from app.services.llm.provider_gemini import GeminiProvider



def _tasks() -> list[dict]:
    return [
        {
            "id": "a",
            "title": "Math Homework",
            "module": "Math",
            "due_at": "2026-02-23T16:00:00Z",
            "module_weight_percent": 40,
            "estimated_hours": 6,
            "notes": "",
        },
        {
            "id": "b",
            "title": "Sport Session",
            "module": "Sport",
            "due_at": "2026-03-20T16:00:00Z",
            "module_weight_percent": 10,
            "estimated_hours": 2,
            "notes": "",
        },
    ]



def test_provider_fallback_shape_when_live_disabled() -> None:
    provider = GeminiProvider(model="gemini-1.5-pro", api_key="", enable_live=False)

    result = provider.rate_tasks(tasks=_tasks(), custom_prompt="", temperature=0.2)

    assert result["provider"] == "gemini"
    assert result["fallback"] is True
    assert isinstance(result["summary"], str)
    assert isinstance(result["rated_tasks"], list)
    assert result["rated_tasks"][0]["priority_score"] >= result["rated_tasks"][1]["priority_score"]



def test_provider_normalizes_live_payload(monkeypatch) -> None:
    provider = GeminiProvider(model="gemini-1.5-pro", api_key="key", enable_live=True)

    def fake_live_call(prompt: str, temperature: float):
        return {
            "summary": "Gemini ranked tasks",
            "ratedTasks": [
                {
                    "id": "b",
                    "priorityScore": "72",
                    "reason": "Sooner than others",
                },
                {
                    "id": "a",
                    "priority_score": 95,
                    "priority_band": "critical",
                    "reason": "Urgent and high weight",
                },
            ],
        }

    monkeypatch.setattr(provider, "_call_live_model", fake_live_call)

    result = provider.rate_tasks(tasks=_tasks(), custom_prompt="test", temperature=0.3)

    assert result["fallback"] is False
    assert result["summary"] == "Gemini ranked tasks"
    assert len(result["rated_tasks"]) == 2
    assert result["rated_tasks"][0]["priority_score"] >= result["rated_tasks"][1]["priority_score"]
    assert {row["id"] for row in result["rated_tasks"]} == {"a", "b"}



def test_provider_uses_heuristic_when_live_output_breaks(monkeypatch) -> None:
    provider = GeminiProvider(model="gemini-1.5-pro", api_key="key", enable_live=True)

    def fake_live_error(prompt: str, temperature: float):
        raise ValueError("broken gemini output")

    monkeypatch.setattr(provider, "_call_live_model", fake_live_error)

    result = provider.rate_tasks(tasks=_tasks(), custom_prompt="test", temperature=0.3)

    assert result["fallback"] is True
    assert result["fallback_reason"] == "broken gemini output"
    assert len(result["rated_tasks"]) == 2

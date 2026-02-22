import json
import re
from typing import Any

from google import genai

from app.services.llm.prompts import build_priority_prompt
from app.utils.time import days_until


class GeminiProvider:
    def __init__(self, model: str, api_key: str = "", enable_live: bool = False) -> None:
        self.model = model
        self.api_key = api_key
        self.enable_live = enable_live
        self.client = (
            genai.Client(api_key=api_key)
            if enable_live and bool(api_key.strip())
            else None
        )

    def _score_band(self, score: int) -> str:
        if score >= 85:
            return "critical"
        if score >= 70:
            return "high"
        if score >= 45:
            return "medium"
        return "low"

    def _clamp_score(self, value: Any) -> int:
        try:
            parsed = int(round(float(value)))
        except Exception:
            parsed = 0
        return max(0, min(100, parsed))

    def _heuristic_rate(self, tasks: list[dict]) -> list[dict]:
        rated = []
        for task in tasks:
            days_left = days_until(task.get("due_at"))
            urgency = max(0, min(100, 100 - (days_left * 8)))
            module_score = max(
                0, min(100, int(task.get("module_weight_percent", 0)) * 2)
            )
            effort_score = max(0, min(100, int(task.get("estimated_hours", 0)) * 9))
            score = round((urgency * 0.55) + (module_score * 0.35) + (effort_score * 0.10))

            rated.append(
                {
                    "id": str(task.get("id", task.get("title", "task"))),
                    "title": str(task.get("title", "Untitled Task")),
                    "priority_score": score,
                    "priority_band": self._score_band(score),
                    "reason": f"Urgency={urgency}, Module={module_score}, Effort={effort_score}",
                }
            )

        rated.sort(key=lambda item: item["priority_score"], reverse=True)
        return rated

    def _extract_response_text(self, response: Any) -> str:
        text = getattr(response, "text", None)
        if isinstance(text, str) and text.strip():
            return text.strip()

        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) or []
            for part in parts:
                value = getattr(part, "text", None)
                if isinstance(value, str) and value.strip():
                    return value.strip()
        raise ValueError("Gemini response did not contain text output")

    def _parse_json_from_text(self, text: str) -> Any:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        match = re.search(r"(\{.*\}|\[.*\])", cleaned, flags=re.DOTALL)
        if not match:
            raise ValueError("Gemini output is not valid JSON")
        return json.loads(match.group(1))

    def _normalize_rated_tasks(self, payload: Any, tasks: list[dict]) -> dict:
        if isinstance(payload, list):
            payload = {"rated_tasks": payload}
        if not isinstance(payload, dict):
            raise ValueError("Gemini output JSON must be an object or array")

        raw_items = (
            payload.get("rated_tasks")
            or payload.get("ratedTasks")
            or payload.get("tasks")
            or []
        )
        if isinstance(raw_items, dict):
            raw_items = [raw_items]
        if not isinstance(raw_items, list):
            raw_items = []

        source_tasks = {
            str(item.get("id", f"task-{idx}")): item
            for idx, item in enumerate(tasks, start=1)
        }
        normalized: list[dict] = []
        used_ids: set[str] = set()

        for idx, item in enumerate(raw_items, start=1):
            if not isinstance(item, dict):
                continue

            task_id = str(
                item.get("id")
                or item.get("task_id")
                or item.get("taskId")
                or f"task-{idx}"
            )
            source = source_tasks.get(task_id, {})
            title = str(item.get("title") or source.get("title") or f"Task {idx}")
            score = self._clamp_score(
                item.get("priority_score")
                or item.get("priorityScore")
                or item.get("score")
            )
            band = str(item.get("priority_band") or item.get("priorityBand") or "").lower()
            if band not in {"critical", "high", "medium", "low"}:
                band = self._score_band(score)
            reason = str(item.get("reason") or "Gemini prioritization")

            normalized.append(
                {
                    "id": task_id,
                    "title": title,
                    "priority_score": score,
                    "priority_band": band,
                    "reason": reason,
                }
            )
            used_ids.add(task_id)

        fallback_entries = self._heuristic_rate(tasks)
        for row in fallback_entries:
            if row["id"] not in used_ids:
                normalized.append(row)

        normalized.sort(key=lambda item: item["priority_score"], reverse=True)
        summary = str(
            payload.get("summary")
            or payload.get("message")
            or f"Prioritized {len(normalized)} tasks"
        )
        return {"summary": summary, "rated_tasks": normalized}

    def _call_live_model(self, prompt: str, temperature: float) -> dict:
        if self.client is None:
            raise ValueError("Live Gemini is disabled or GEMINI_API_KEY is missing")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"temperature": float(temperature)},
        )
        text = self._extract_response_text(response)
        payload = self._parse_json_from_text(text)
        return payload if isinstance(payload, dict) else {"rated_tasks": payload}

    def rate_tasks(
        self,
        tasks: list[dict],
        custom_prompt: str = "",
        temperature: float = 0.2,
    ) -> dict:
        if not tasks:
            return {
                "provider": "gemini",
                "model": self.model,
                "fallback": True,
                "summary": "No tasks were provided",
                "rated_tasks": [],
                "fallback_reason": "NO_TASKS",
                "prompt_used": custom_prompt,
                "temperature": temperature,
            }

        prompt = build_priority_prompt(tasks=tasks, custom_prompt=custom_prompt)
        fallback = False
        fallback_reason = None

        try:
            live_payload = self._call_live_model(prompt=prompt, temperature=temperature)
            normalized = self._normalize_rated_tasks(payload=live_payload, tasks=tasks)
        except Exception as exc:
            fallback = True
            fallback_reason = str(exc)
            normalized = {
                "summary": "Heuristic fallback mode used",
                "rated_tasks": self._heuristic_rate(tasks),
            }

        return {
            "provider": "gemini",
            "model": self.model,
            "fallback": fallback,
            "summary": normalized["summary"],
            "rated_tasks": normalized["rated_tasks"],
            "fallback_reason": fallback_reason,
            "prompt_used": custom_prompt,
            "temperature": temperature,
        }

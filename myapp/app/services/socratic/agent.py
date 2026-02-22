import json
import re
from pathlib import Path
from typing import Any

from google import genai

from app.services.socratic.chunker import (
    chunk_by_paragraphs,
    chunk_by_sentences,
    chunk_text,
)


class SocraticAgentService:
    _RED_FLAG_PATTERNS = [
        r"\b(write|complete|do|solve) (my|this|the) (assignment|essay|coursework|homework)\b",
        r"\b(give|provide|show) (me )?(the )?(answer|solution|code)\b",
        r"\bwrite.*for me\b",
        r"\bcomplete.*assignment\b",
        r"\bgive.*full (code|essay|solution)\b",
    ]

    _TECHNICAL_SKILLS = [
        "python",
        "java",
        "javascript",
        "typescript",
        "sql",
        "mongodb",
        "postgresql",
        "machine learning",
        "data analysis",
        "rest api",
        "fastapi",
        "react",
    ]
    _TOOLS = [
        "git",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "linux",
        "jira",
        "figma",
        "power bi",
    ]
    _COGNITIVE = [
        "problem solving",
        "analytical thinking",
        "critical thinking",
        "attention to detail",
        "debugging",
        "reasoning",
    ]
    _BEHAVIOURAL = [
        "communication",
        "teamwork",
        "collaboration",
        "leadership",
        "adaptability",
        "stakeholder management",
    ]

    def __init__(
        self,
        model: str,
        api_key: str = "",
        enable_live: bool = False,
        prompt_dir: Path | None = None,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.enable_live = bool(enable_live and api_key.strip())
        self.client = genai.Client(api_key=api_key) if self.enable_live else None
        self.prompt_dir = prompt_dir or (Path(__file__).resolve().parent / "prompts")

    def _load_prompt(self, name: str) -> str:
        path = self.prompt_dir / name
        return path.read_text(encoding="utf-8")

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

    def _generate_text(self, prompt: str, temperature: float) -> str:
        if self.client is None:
            raise ValueError("Live Gemini is disabled")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"temperature": float(temperature)},
        )
        return self._extract_response_text(response)

    def _matches_red_flag(self, query: str) -> bool:
        for pattern in self._RED_FLAG_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False

    def _ai_integrity_assessment(self, query: str) -> dict:
        prompt = f"""You are an academic integrity officer at a UK Russell Group university.

Assess if this student query violates academic integrity policies.

Query: "{query}"

Determine:
1. Is the student asking for direct assignment completion?
2. Or are they seeking legitimate learning support?

Legitimate: concept explanations, debugging guidance, methodology questions.
Violation: requests for complete solutions, essay writing, direct answers.

Respond with ONLY one label:
ACCEPTABLE
VIOLATION
"""
        result = self._generate_text(prompt=prompt, temperature=0.1).strip().upper()
        if "VIOLATION" in result:
            return {
                "is_acceptable": False,
                "reason": "AI detected potential academic integrity violation",
                "severity": "medium",
            }
        return {
            "is_acceptable": True,
            "reason": "Query is a legitimate learning request",
            "severity": "none",
        }

    def check_academic_integrity(self, student_query: str) -> dict:
        if self._matches_red_flag(student_query):
            return {
                "is_acceptable": False,
                "reason": "Request appears to seek direct assignment completion",
                "severity": "high",
            }

        if not self.enable_live:
            return {
                "is_acceptable": True,
                "reason": "Heuristic check passed (live integrity model disabled)",
                "severity": "none",
            }

        try:
            return self._ai_integrity_assessment(student_query)
        except Exception:
            return {
                "is_acceptable": True,
                "reason": "Could not assess - defaulting to acceptable",
                "severity": "unknown",
            }

    def _fallback_socratic_question(self, topic: str, previous_answer: str | None) -> str:
        if previous_answer and previous_answer.strip():
            clipped = previous_answer.strip().splitlines()[0][:120]
            return (
                f"You said: '{clipped}'. Which assumption in that answer matters most "
                f"for {topic}, and how could you test it with evidence?"
            )
        return (
            f"For {topic}, what core principle must be true before any solution works, "
            "and why?"
        )

    def socratic_viva(
        self,
        topic: str,
        previous_answer: str | None = None,
        student_query: str | None = None,
    ) -> dict:
        integrity = (
            self.check_academic_integrity(student_query)
            if student_query and student_query.strip()
            else None
        )
        if integrity and not integrity["is_acceptable"]:
            return {
                "question": (
                    "I cannot complete assignments for you. "
                    f"Instead, what have you already tried on '{topic}'?"
                ),
                "fallback": True,
                "integrity": integrity,
            }

        prompt_template = self._load_prompt("socratic_viva.txt")
        prompt = prompt_template.format(
            topic=topic,
            previous_answer=previous_answer or "No prior response.",
        )

        try:
            question = self._generate_text(prompt=prompt, temperature=0.4)
            return {"question": question, "fallback": False, "integrity": integrity}
        except Exception:
            question = self._fallback_socratic_question(topic=topic, previous_answer=previous_answer)
            return {"question": question, "fallback": True, "integrity": integrity}

    def _extract_json_safely(self, text: str) -> dict:
        cleaned = text.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        markdown_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
        if markdown_match:
            try:
                return json.loads(markdown_match.group(1))
            except json.JSONDecodeError:
                pass

        object_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if object_match:
            return json.loads(object_match.group(0))

        raise ValueError("Could not parse JSON from model output")

    def _normalize_text_list(self, values: Any) -> list[str]:
        if not isinstance(values, list):
            return []
        normalized: list[str] = []
        seen: set[str] = set()
        for value in values:
            item = str(value).strip()
            key = item.lower()
            if not item or key in seen:
                continue
            seen.add(key)
            normalized.append(item)
        return normalized

    def _validate_career_schema(self, data: dict) -> None:
        required_fields = {
            "technical_skills": list,
            "tools_technologies": list,
            "cognitive_skills": list,
            "behavioural_traits": list,
            "experience_level": str,
        }
        for field, expected_type in required_fields.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(data[field], expected_type):
                raise ValueError(
                    f"Field '{field}' must be {expected_type.__name__}, got "
                    f"{type(data[field]).__name__}"
                )

    def _collect_keywords(self, text: str, keywords: list[str]) -> list[str]:
        text_lower = text.lower()
        found: list[str] = []
        for keyword in keywords:
            if keyword in text_lower:
                found.append(keyword.title())
        return found

    def _infer_experience_level(self, text: str) -> str:
        text_lower = text.lower()
        if re.search(r"\b(senior|lead|principal|5\+ years|7\+ years)\b", text_lower):
            return "Senior"
        if re.search(r"\b(junior|graduate|entry|intern|0-2 years)\b", text_lower):
            return "Graduate / Entry-level"
        if re.search(r"\b(mid|3\+ years|4\+ years)\b", text_lower):
            return "Mid-level"
        return "Not specified"

    def _heuristic_career_analysis(self, job_text: str) -> dict:
        return {
            "technical_skills": self._collect_keywords(job_text, self._TECHNICAL_SKILLS),
            "tools_technologies": self._collect_keywords(job_text, self._TOOLS),
            "cognitive_skills": self._collect_keywords(job_text, self._COGNITIVE),
            "behavioural_traits": self._collect_keywords(job_text, self._BEHAVIOURAL),
            "experience_level": self._infer_experience_level(job_text),
            "fallback": True,
        }

    def analyze_career_match(self, job_text: str) -> dict:
        prompt_template = self._load_prompt("career_analysis.txt")
        prompt = prompt_template.format(job_text=job_text)

        if not self.enable_live:
            return self._heuristic_career_analysis(job_text=job_text)

        try:
            raw_text = self._generate_text(prompt=prompt, temperature=0.2)
            parsed_json = self._extract_json_safely(raw_text)
            self._validate_career_schema(parsed_json)
            parsed_json["technical_skills"] = self._normalize_text_list(
                parsed_json.get("technical_skills")
            )
            parsed_json["tools_technologies"] = self._normalize_text_list(
                parsed_json.get("tools_technologies")
            )
            parsed_json["cognitive_skills"] = self._normalize_text_list(
                parsed_json.get("cognitive_skills")
            )
            parsed_json["behavioural_traits"] = self._normalize_text_list(
                parsed_json.get("behavioural_traits")
            )
            parsed_json["experience_level"] = str(
                parsed_json.get("experience_level", "Not specified")
            )
            parsed_json["fallback"] = False
            return parsed_json
        except Exception:
            return self._heuristic_career_analysis(job_text=job_text)

    def chunk_text(self, text: str, max_chunk_size: int = 1000, overlap: int = 100) -> list[str]:
        return chunk_text(text=text, max_chunk_size=max_chunk_size, overlap=overlap)

    def chunk_by_sentences(self, text: str, sentences_per_chunk: int = 5) -> list[str]:
        return chunk_by_sentences(text=text, sentences_per_chunk=sentences_per_chunk)

    def chunk_by_paragraphs(self, text: str, max_paragraphs: int = 3) -> list[str]:
        return chunk_by_paragraphs(text=text, max_paragraphs=max_paragraphs)

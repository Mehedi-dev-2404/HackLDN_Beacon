from app.models.domain.job import Job
from app.models.domain.task import Task
from app.models.persistence.job_repo import JobRepository
from app.models.persistence.task_repo import TaskRepository
from app.services.llm.provider_gemini import GeminiProvider
from app.services.scraping.browser_scraper import BrowserScraper
from app.services.scraping.http_scraper import HttpScraper
from app.services.scraping.parser import parse_assignments
from app.utils.hashing import sha256_text


class WorkflowPipeline:
    def __init__(
        self,
        job_repo: JobRepository,
        task_repo: TaskRepository,
        llm_provider: GeminiProvider,
    ) -> None:
        self.job_repo = job_repo
        self.task_repo = task_repo
        self.llm_provider = llm_provider
        self.http_scraper = HttpScraper()
        self.browser_scraper = BrowserScraper()

    def run_scrape(self, source_url: str, mode: str, raw_html: str = "") -> dict:
        scraper = self.browser_scraper if mode == "browser" else self.http_scraper
        source, html = scraper.scrape(source_url=source_url, raw_html=raw_html)
        assignments = parse_assignments(html)

        return {
            "source": source,
            "mode": mode,
            "assignment_count": len(assignments),
            "assignments": assignments,
            "hash": sha256_text(html),
        }

    def persist_assignments(self, assignments: list[dict]) -> int:
        jobs = [
            Job(
                id=f"job-{index}",
                title=item["title"],
                module=item["module"],
                due_at=item.get("due_at"),
                module_weight_percent=int(item.get("module_weight_percent", 0)),
                estimated_hours=int(item.get("estimated_hours", 0)),
                notes=item.get("notes", ""),
            )
            for index, item in enumerate(assignments, start=1)
        ]
        return self.job_repo.upsert_jobs(jobs)

    def _build_llm_tasks(self, assignments: list[dict]) -> list[dict]:
        tasks = []
        for index, item in enumerate(assignments, start=1):
            tasks.append(
                {
                    "id": f"task-{index}",
                    "title": item["title"],
                    "module": item.get("module", "General"),
                    "due_at": item.get("due_at"),
                    "module_weight_percent": item.get("module_weight_percent", 0),
                    "estimated_hours": item.get("estimated_hours", 0),
                    "notes": item.get("notes", ""),
                }
            )
        return tasks

    def run_llm(self, assignments: list[dict], custom_prompt: str = "") -> dict:
        tasks = self._build_llm_tasks(assignments)

        return self.llm_provider.rate_tasks(tasks=tasks, custom_prompt=custom_prompt)

    def _parse_priority(self, value: object) -> int:
        try:
            parsed = int(round(float(value)))
        except Exception:
            parsed = 1
        return max(1, min(100, parsed))

    def persist_ranked_tasks(self, llm_output: dict, source_tasks: list[dict]) -> int:
        rated_tasks = llm_output.get("rated_tasks", [])
        if not isinstance(rated_tasks, list):
            return 0

        source_by_id = {
            str(item.get("id", f"task-{index}")): item
            for index, item in enumerate(source_tasks, start=1)
            if isinstance(item, dict)
        }

        tasks: list[Task] = []
        for index, item in enumerate(rated_tasks, start=1):
            if not isinstance(item, dict):
                continue

            task_id = str(item.get("id", f"task-{index}"))
            source = source_by_id.get(task_id, {})
            title = str(item.get("title") or source.get("title") or f"Task {index}")
            subject = str(source.get("module", "General"))
            deadline = str(source.get("due_at") or "")
            priority = self._parse_priority(item.get("priority_score", 1))

            tasks.append(
                Task(
                    id=task_id,
                    title=title,
                    subject=subject,
                    deadline=deadline,
                    priority=priority,
                )
            )

        return self.task_repo.upsert_tasks(tasks)

    def run(self, source_url: str, raw_html: str, scrape_mode: str, custom_prompt: str = "") -> dict:
        scrape_output = self.run_scrape(source_url=source_url, mode=scrape_mode, raw_html=raw_html)
        persisted_jobs = self.persist_assignments(scrape_output["assignments"])
        llm_tasks = self._build_llm_tasks(scrape_output["assignments"])
        llm_output = self.llm_provider.rate_tasks(tasks=llm_tasks, custom_prompt=custom_prompt)
        persisted_tasks = self.persist_ranked_tasks(llm_output=llm_output, source_tasks=llm_tasks)

        return {
            "scrape": scrape_output,
            "llm": llm_output,
            "persisted_jobs": persisted_jobs,
            "persisted_tasks": persisted_tasks,
        }

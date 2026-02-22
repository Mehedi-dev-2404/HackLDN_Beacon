import os

import pytest

from app.core.dependencies import get_job_repo, get_task_repo, get_workflow_pipeline
from app.main import app
from app.models.domain.job import Job
from app.models.domain.task import Task
from app.services.llm.provider_gemini import GeminiProvider
from app.services.workflow.pipeline import WorkflowPipeline


# Phase-1 startup checks require these env vars.
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("DB_NAME", "beacon_test")
os.environ.setdefault("TASKS_DB_NAME", "beacon_tasks_test")
os.environ.setdefault("ENABLE_LIVE_LLM", "0")


class InMemoryJobRepo:
    def __init__(self) -> None:
        self._store: dict[str, Job] = {}

    def upsert_jobs(self, jobs: list[Job]) -> int:
        for job in jobs:
            self._store[job.id] = job
        return len(jobs)

    def replace_jobs(self, jobs: list[Job]) -> int:
        return self.upsert_jobs(jobs)

    def list_jobs(self, limit: int = 200) -> list[Job]:
        values = list(self._store.values())
        return values[: max(1, int(limit))]


class InMemoryTaskRepo:
    def __init__(self) -> None:
        self._store: dict[str, Task] = {}

    def upsert_tasks(self, tasks: list[Task]) -> int:
        for task in tasks:
            self._store[task.id] = task
        return len(tasks)

    def replace_tasks(self, tasks: list[Task]) -> int:
        return self.upsert_tasks(tasks)

    def list_tasks(self, limit: int = 200) -> list[Task]:
        values = list(self._store.values())
        return values[: max(1, int(limit))]


@pytest.fixture(autouse=True)
def override_runtime_dependencies():
    repo = InMemoryJobRepo()
    task_repo = InMemoryTaskRepo()
    provider = GeminiProvider(model="gemini-1.5-pro", api_key="test", enable_live=False)
    pipeline = WorkflowPipeline(job_repo=repo, task_repo=task_repo, llm_provider=provider)

    app.dependency_overrides[get_job_repo] = lambda: repo
    app.dependency_overrides[get_task_repo] = lambda: task_repo
    app.dependency_overrides[get_workflow_pipeline] = lambda: pipeline
    yield
    app.dependency_overrides.clear()

from app.models.domain.job import Job
from app.models.persistence.job_repo import JobRepository


class _FakeCursor:
    def __init__(self, rows: list[dict]) -> None:
        self.rows = rows

    def sort(self, key: str, direction: int):
        reverse = direction == -1
        self.rows.sort(key=lambda row: row.get(key, ""), reverse=reverse)
        return self

    def limit(self, value: int):
        self.rows = self.rows[:value]
        return self

    def __iter__(self):
        return iter(self.rows)


class _FakeCollection:
    def __init__(self) -> None:
        self.docs: dict[str, dict] = {}

    def update_one(self, query: dict, update: dict, upsert: bool = False) -> None:
        job_id = query["job_id"]
        existing = self.docs.get(job_id)

        if existing is None:
            existing = {}
            existing.update(update.get("$setOnInsert", {}))

        existing.update(update.get("$set", {}))
        self.docs[job_id] = existing

    def find(self, _query: dict, _projection: dict):
        rows = [dict(row) for row in self.docs.values()]
        return _FakeCursor(rows)



def test_job_repo_upsert_and_list_are_deterministic() -> None:
    fake_collection = _FakeCollection()
    repo = JobRepository(
        mongo_uri="mongodb://localhost:27017",
        db_name="beacon_test",
        collection=fake_collection,
    )

    first = Job(
        id="job-1",
        title="Math",
        module="Math",
        due_at=None,
        module_weight_percent=40,
        estimated_hours=4,
        notes="",
    )
    second = Job(
        id="job-2",
        title="Business",
        module="Business",
        due_at=None,
        module_weight_percent=20,
        estimated_hours=2,
        notes="",
    )

    assert repo.upsert_jobs([first, second]) == 2

    updated_first = Job(
        id="job-1",
        title="Math Updated",
        module="Math",
        due_at=None,
        module_weight_percent=45,
        estimated_hours=5,
        notes="updated",
    )
    assert repo.upsert_jobs([updated_first]) == 1

    jobs = repo.list_jobs(limit=10)
    by_id = {job.id: job for job in jobs}
    assert len(by_id) == 2
    assert by_id["job-1"].title == "Math Updated"
    assert by_id["job-1"].module_weight_percent == 45

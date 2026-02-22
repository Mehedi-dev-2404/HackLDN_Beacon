from app.core.dependencies import get_job_repo
from app.models.domain.job import Job



def main() -> None:
    repo = get_job_repo()
    seeded = [
        Job(
            id="job-1",
            title="Macroeconomics Essay",
            module="Economics",
            due_at="2026-02-23T16:00:00Z",
            module_weight_percent=45,
            estimated_hours=8,
            notes="Seeded task",
        ),
        Job(
            id="job-2",
            title="Python Practice for Technical Test",
            module="Career",
            due_at="2026-02-24T18:00:00Z",
            module_weight_percent=30,
            estimated_hours=5,
            notes="Seeded task",
        ),
    ]
    count = repo.upsert_jobs(seeded)
    print(f"Seeded {count} jobs")


if __name__ == "__main__":
    main()

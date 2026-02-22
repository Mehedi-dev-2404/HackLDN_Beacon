# myapp

FastAPI backend restructured into layered modules:

- `app/main.py`: FastAPI entrypoint
- `app/core`: config, logging, dependencies, exceptions
- `app/view/v1`: routers + endpoints
- `app/viewmodels`: response shaping and view-level logic
- `app/models`: domain objects, schemas, persistence
- `app/services`: scraping, llm, workflow orchestration
- `app/utils`: shared helpers
- `scripts`: worker and seed scripts
- `tests`: API tests for scrape + llm

## Run

```bash
cd myapp
python3 -m uvicorn app.main:app --reload
```

Required env vars for startup checks:

- `GEMINI_API_KEY`
- `MONGO_URI`
- `DB_NAME` (or `JOBS_DB_NAME`) for jobs database
- `TASKS_DB_NAME` for tasks database

Open:

- API docs: `http://127.0.0.1:8000/docs`
- UI panel switcher: `http://127.0.0.1:8000/api/v1/health/ui`
- Each non-dashboard panel page includes an API playground (request body + run button + live response view).

Socratic agent endpoints:

- `POST /api/v1/socratic/question`
- `POST /api/v1/socratic/integrity-check`
- `POST /api/v1/socratic/career-analysis`
- `POST /api/v1/socratic/chunk`
- `POST /api/v1/socratic/voice`

## Notes

- Dashboard page reuses `Mohammed/code.html`.
- Panel page adds switching between Dashboard, Health, Scrape, LLM, and Workflow views.
- LLM module is Gemini-only and currently uses deterministic heuristic scoring in `app/services/llm/provider_gemini.py`.
- Socratic module ports Mehedi's questioning, integrity checks, career extraction, and text chunking in `app/services/socratic`.
- Persistence is MongoDB-backed via `app/models/persistence/db.py` and `app/models/persistence/job_repo.py`.
- Jobs are written to the jobs database (`DB_NAME` / `JOBS_DB_NAME`) and tasks are written to the tasks database (`TASKS_DB_NAME`).
- Task schema follows Rahul's structure: `id`, `title`, `subject`, `deadline`, `priority`.

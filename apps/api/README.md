# Beacon API

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
cd apps/api
python3 -m pip install -e ".[dev]"
python3 -m uvicorn app.main:app --reload --port 8000
```

Required env vars for startup checks:

- `GEMINI_API_KEY`
- `MONGO_URI`
- `DB_NAME` (or `JOBS_DB_NAME`) for jobs database
- `TASKS_DB_NAME` for tasks database
- `DOCS_DB_NAME` for document metadata + GridFS
- `DEFAULT_USER_ID` for single-user MVP routing
- `SCHEDULE_TIMEZONE` for scheduler slots
- `MAX_UPLOAD_MB` for PDF upload limit
- `SERPAPI_KEY` (required for LinkedIn discovery endpoints)
- `FRONTEND_BASE_URL` for `/app` redirect target

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/v1/health`
- Frontend redirect: `http://127.0.0.1:8000/app`

Socratic agent endpoints:

- `POST /api/v1/socratic/question`
- `POST /api/v1/socratic/integrity-check`
- `POST /api/v1/socratic/career-analysis`
- `POST /api/v1/socratic/chunk`
- `POST /api/v1/socratic/voice`

New integrated endpoints:

- Scheduler: `GET /api/v1/scheduler/events`, `POST /api/v1/scheduler/tasks`, `PATCH /api/v1/scheduler/tasks/{task_id}`, `POST /api/v1/scheduler/reschedule`
- Documents: `POST /api/v1/documents/lecture-notes/upload`, `POST /api/v1/documents/academic-reports/upload`, `GET /api/v1/documents/lecture-notes`, `GET /api/v1/documents/academic-reports`, `GET /api/v1/documents/{doc_id}/download`
- Assistant: `POST /api/v1/assistant/chat`
- Jobs: `POST /api/v1/jobs/discover`, `GET /api/v1/jobs`, `POST /api/v1/jobs/refresh`

## Notes

- LLM module is Gemini-only and currently uses deterministic heuristic scoring in `app/services/llm/provider_gemini.py`.
- Socratic module ports the original hackathon questioning, integrity checks, career extraction, and text chunking in `app/services/socratic`.
- Persistence is MongoDB-backed via `app/models/persistence/db.py` and `app/models/persistence/job_repo.py`.
- Jobs are written to the jobs database (`DB_NAME` / `JOBS_DB_NAME`) and tasks are written to the tasks database (`TASKS_DB_NAME`).
- Frontend is deployed separately from `apps/web` and targets this API via `runtime-config.js`.

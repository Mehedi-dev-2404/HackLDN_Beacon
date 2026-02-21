# Tom - Member 4 Task Runner (React)

Basic React UI to run Member 4 hackathon tasks from `idea.pdf`:
- Moodle sync
- Career sync / JSON inject
- Data cleaning + schema mapping
- LLM priority scoring (due date + module weighting)
- Golden-path demo seed

## Quick Start

```bash
cd Tom
npm install
npm run dev
```

## Tiny Backend (LLM Proxy)

Use this when you want `/member4/llm-priority` to run server-side (recommended so keys are not in browser).

1. Create env file:

```bash
cd Tom
cp .env.example .env
```

2. Add Gemini key in `.env`:
- `GEMINI_API_KEY=...`

3. Run backend:

```bash
cd Tom
npm run dev:backend
```

4. Run frontend in another terminal:

```bash
cd Tom
npm run dev
```

5. In UI, set `Backend API Base URL` to:
- `http://127.0.0.1:8000`

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Hackathon Structure Choice

This project uses **MVVM (feature-first)** because it keeps UI speed high while staying organized:

- `views/` for screen components
- `viewmodels/` for state + action logic
- `services/` for API calls + mock fallback
- `models/` for task metadata and shared shapes

This is practical in a hackathon because:
- UI can ship fast with mock data first
- backend can plug in later by replacing service endpoints
- team members can work in parallel without stepping on each other

## Folder Layout

```txt
Tom/
  backend/
    server.mjs
  src/
    features/
      member4/
        models/
          member4Tasks.js
        services/
          member4Service.js
        viewmodels/
          useMember4ViewModel.js
        views/
          Member4Dashboard.jsx
    shared/
      components/
        TaskCard.jsx
    App.jsx
    main.jsx
    styles.css
```

## API Endpoints Expected (optional)

If you provide a backend base URL, these POST routes are used:
- `/member4/moodle-sync`
- `/member4/career-sync`
- `/member4/clean-map`
- `/member4/llm-priority`
- `/member4/demo-seed`

Tiny backend included in `backend/server.mjs` currently implements:
- `GET /health`
- `GET /member4/llm-priority/file`
- `POST /member4/llm-priority`

If any call fails, the UI automatically switches to mock mode so demo flow still works.

## LLM Priority Tuning

The dashboard includes controls for:
- Model name
- Temperature
- Custom prompt
- Rubric weights (`deadlineWeight`, `moduleWeight`, `effortWeight`)

You can run through:
- Backend proxy (`/member4/llm-priority`) - recommended
- Direct browser Gemini API call with your own key - useful for rapid hackathon experiments

## Why This Backend Route

- Keeps LLM API keys off the frontend.
- Uses a single Gemini path for consistent outputs.
- Adds a safe heuristic fallback so demo still works if LLM call fails.
- Persists latest output to `backend/data/llm_priority_latest.json` for easy frontend extraction.

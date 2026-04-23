# Beacon

An AI-powered student OS that combines Socratic tutoring, career preparation, and intelligent task management — helping students manage academic pressure and graduate scheme deadlines.

## Repo Layout

```text
apps/
  api/    FastAPI backend
  web/    Static Beacon frontend
archive/  Archived hackathon spikes and contributor workspaces
docker/   Container build definitions
docs/     Architecture and deployment docs
infra/    Terraform for AWS deployment
scripts/  Local helper scripts
```

## Features

- **Socratic Mirror** — AI tutor that asks questions instead of giving answers, with academic integrity checking and voice synthesis
- **Career CRM** — Analyses job descriptions to extract skills and maps them against your profile
- **Assignment Pipeline** — Scrapes Moodle and ranks tasks by urgency, module weight, and effort

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python |
| Frontend | HTML, Tailwind CSS |
| AI / LLM | Google Gemini 1.5 Pro |
| Voice | ElevenLabs |
| Database | MongoDB Atlas |

## Running Locally

```bash
# Option 1: Docker
docker compose up --build

# Option 2: Run services directly
cd apps/api && python3 -m pip install -e ".[dev]"
python3 -m uvicorn app.main:app --reload --port 8000

# In another terminal
bash scripts/render-web-config.sh http://localhost:8000/api/v1
# Then open apps/web/index.html via any static file server or the web container
```

Required configuration:

- `apps/api/.env` for backend secrets and database settings
- `apps/web/runtime-config.js` for frontend API targeting

See:

- [`apps/api/.env.example`](/Users/nguyencongkhanh/HackLDN_Beacon/apps/api/.env.example)
- [`apps/web/.env.example`](/Users/nguyencongkhanh/HackLDN_Beacon/apps/web/.env.example)
- [`docs/architecture.md`](/Users/nguyencongkhanh/HackLDN_Beacon/docs/architecture.md)
- [`docs/deployment-aws.md`](/Users/nguyencongkhanh/HackLDN_Beacon/docs/deployment-aws.md)

## Deployment

- Frontend: S3 + CloudFront
- Backend: ECS Fargate + ALB + ECR
- Secrets: AWS Secrets Manager
- Infrastructure: Terraform in [`infra/terraform`](/Users/nguyencongkhanh/HackLDN_Beacon/infra/terraform)

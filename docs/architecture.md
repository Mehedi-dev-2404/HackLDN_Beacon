# Beacon Architecture

Beacon is split into two deployable surfaces:

- `apps/web`: static Beacon UI served from object storage/CDN
- `apps/api`: FastAPI backend exposing `/api/v1/*`

## Runtime model

- Frontend reads `window.BEACON_CONFIG.API_BASE_URL` from `runtime-config.js`
- Backend remains stateless and can scale horizontally
- MongoDB Atlas is the production data store
- Secrets are injected through environment variables

## Local development

- `docker compose up --build` runs `web`, `api`, and `mongo`
- The backend redirects `/app` to `FRONTEND_BASE_URL`
- The frontend calls the API via `API_BASE_URL`

## Active vs archived code

- `apps/` contains production code only
- `archive/` contains historical hackathon work that is intentionally not referenced by Docker, Terraform, or CI

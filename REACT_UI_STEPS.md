# React UI Setup

Copy `frontend/` and `docker-compose.react.yml` into the project root.

Run locally:

```powershell
docker compose -f docker-compose.react.yml up --build
```

Open:

```text
http://localhost:3000
```

Railway React UI service variables:

```text
RAILWAY_DOCKERFILE_PATH=frontend/Dockerfile
TRIAGE_API_URL=https://YOUR-TRIAGE-AGENT-DOMAIN/triage
```

This React UI replaces the Streamlit UI.

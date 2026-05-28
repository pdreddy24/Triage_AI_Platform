# Live Deployment Steps

## 1. Replace/add files
Copy these files into your project root. When Windows asks whether to replace existing files, choose **Replace**.

## 2. Run locally with Docker
From the project root:

```bash
docker compose -f docker-compose.live.yml up --build
```

Open:

- UI: http://localhost:8501
- Triage API docs: http://localhost:8003/docs
- Scoring health: http://localhost:8001/health
- Graph health: http://localhost:8002/health

## 3. Deploy live
For a beginner-friendly deployment, push the project to GitHub and deploy the Docker services on Railway or Render.

You need these public services:

1. scoring-service
2. graph-service
3. triage-agent
4. ui

For the live UI, set this environment variable:

```text
TRIAGE_API_URL=https://YOUR-TRIAGE-AGENT-URL/triage
```

For the live triage-agent, set:

```text
SCORING_URL=https://YOUR-SCORING-SERVICE-URL/score
GRAPH_URL=https://YOUR-GRAPH-SERVICE-URL/analyze
```

## Important
This makes the project deployable as a demo. For real production, add authentication, persistent database storage, proper model files, secrets management, and rate limiting.

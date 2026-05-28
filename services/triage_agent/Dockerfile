FROM python:3.11-slim

WORKDIR /app

COPY services/triage_agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/triage_agent /app

EXPOSE 8003

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]

FROM python:3.12-slim

WORKDIR /app

# Set Python path so agents module is discoverable
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY agents /app/agents
COPY triage_api.py /app/

EXPOSE 8000

CMD ["uvicorn", "triage_api:app", "--host", "0.0.0.0", "--port", "8000"]
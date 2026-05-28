FROM python:3.11

WORKDIR /app

COPY services/graph_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/graph_service /app

EXPOSE 8002

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
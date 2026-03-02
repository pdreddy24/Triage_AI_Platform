import schedule
import time
from data_engineering.graph_pipeline.embedding_refresh_job import refresh_embeddings


def start_scheduler():
    schedule.every(10).minutes.do(refresh_embeddings)

    while True:
        schedule.run_pending()
        time.sleep(1)
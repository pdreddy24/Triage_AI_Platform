from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter
import time


# Custom metrics
score_latency = Histogram(
    "score_endpoint_latency_seconds",
    "Latency of score endpoint"
)

score_requests = Counter(
    "score_requests_total",
    "Total score endpoint calls"
)

score_errors = Counter(
    "score_errors_total",
    "Total score endpoint errors"
)


def setup_metrics(app):
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
    ).instrument(app).expose(app)
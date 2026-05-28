import json
import time


def simulate_stream(file_path: str, delay=0.2):
    with open(file_path) as f:
        for line in f:
            yield json.loads(line)
            time.sleep(delay)
from locust import HttpUser, task, between
import random
import datetime


class FraudUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        response = self.client.post("/login")
        self.token = response.json()["access_token"]

    @task
    def score_transaction(self):
        payload = {
            "transaction_id": f"tx-{random.randint(1,100000)}",
            "user_id": 1,
            "device_id": 1,
            "merchant_id": 10,
            "amount": random.randint(10, 1000),
            "timestamp": datetime.datetime.now().isoformat()
        }

        self.client.post(
            "/api/score",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"}
        )
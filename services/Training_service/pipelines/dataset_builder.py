# training_service/pipelines/dataset_builder.py

import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random


def build_training_dataset(output_path: str,
                           n_users: int = 1000,
                           n_transactions: int = 20000,
                           fraud_ratio: float = 0.05):

    np.random.seed(42)
    random.seed(42)

    users = [f"user_{i}" for i in range(n_users)]
    devices = [f"device_{i}" for i in range(n_users * 2)]
    merchants = [f"merchant_{i}" for i in range(200)]
    ips = [f"10.0.{i//255}.{i%255}" for i in range(n_users * 2)]

    fraud_ring_devices = random.sample(devices, 40)
    fraud_ring_ips = random.sample(ips, 40)

    transactions = []
    start_time = datetime.utcnow()

    for _ in range(n_transactions):

        is_fraud = np.random.rand() < fraud_ratio
        user = random.choice(users)

        if is_fraud:
            device = random.choice(fraud_ring_devices)
            ip = random.choice(fraud_ring_ips)
            amount = np.random.exponential(400)
            country = "NG"
            billing_country = "US"
        else:
            device = random.choice(devices)
            ip = random.choice(ips)
            amount = np.random.exponential(80)
            country = "US"
            billing_country = "US"

        timestamp = start_time + timedelta(
            minutes=random.randint(0, 20000)
        )

        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "user_id": user,
            "device_id": device,
            "merchant_id": random.choice(merchants),
            "ip_address": ip,
            "amount": round(amount, 2),
            "timestamp": timestamp,
            "country_code": country,
            "billing_country": billing_country,
            "channel": random.choice(["web", "mobile", "atm"]),
            "is_fraud": int(is_fraud),
        })

    df = pd.DataFrame(transactions)
    df.to_parquet(output_path)
import pandas as pd


def load_transactions_from_parquet(path: str):
    return pd.read_parquet(path)
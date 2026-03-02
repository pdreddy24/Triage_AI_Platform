# training_service/pipelines/calibration_pipeline.py

import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score


def calibrate_model(model_path: str,
                    dataset_path: str,
                    embeddings_path: str):

    model = joblib.load(model_path)

    df = pd.read_parquet(dataset_path)
    emb_df = pd.read_parquet(embeddings_path)

    # Merge embeddings
    df = df.merge(emb_df, on="user_id", how="left")

    # Feature engineering (must match GBT pipeline)
    df["country_mismatch"] = (
        df["country_code"] != df["billing_country"]
    ).astype(int)

    df = pd.get_dummies(df, columns=["channel"], drop_first=True)

    feature_cols = []

    feature_cols.append("amount")
    feature_cols.append("country_mismatch")

    channel_cols = [c for c in df.columns if c.startswith("channel_")]
    feature_cols.extend(channel_cols)

    embedding_cols = [c for c in df.columns if c.startswith("emb_")]
    feature_cols.extend(embedding_cols)

    X = df[feature_cols]
    y = df["is_fraud"]

    preds = model.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, preds)

    return {"auc": auc}
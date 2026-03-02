# training_service/pipelines/gbt_pipeline.py

import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


def train_gbt(dataset_path: str,
              embeddings_path: str,
              model_output_path: str):

    # Load dataset
    df = pd.read_parquet(dataset_path)

    # Load embeddings
    emb_df = pd.read_parquet(embeddings_path)

    # Merge on user_id
    df = df.merge(emb_df, on="user_id", how="left")

    # Basic feature engineering
    df["country_mismatch"] = (
        df["country_code"] != df["billing_country"]
    ).astype(int)

    # One-hot encode channel
    df = pd.get_dummies(df, columns=["channel"], drop_first=True)

    # Select features
    feature_cols = []

    # Transaction-level
    feature_cols.append("amount")
    feature_cols.append("country_mismatch")

    # Channel columns
    channel_cols = [c for c in df.columns if c.startswith("channel_")]
    feature_cols.extend(channel_cols)

    # Graph embedding columns
    embedding_cols = [c for c in df.columns if c.startswith("emb_")]
    feature_cols.extend(embedding_cols)

    X = df[feature_cols]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = lgb.LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=64,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)

    print(f"GBT AUC: {auc:.4f}")

    joblib.dump(model, model_output_path)
import joblib


class ScoringModel:

    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, features: list) -> float:
        return float(self.model.predict_proba([features])[0][1])
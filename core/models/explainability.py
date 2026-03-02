import shap
import numpy as np


class Explainer:

    def __init__(self, model):
        self.explainer = shap.TreeExplainer(model)

    def explain(self, features: list):
        shap_values = self.explainer.shap_values(np.array([features]))
        return shap_values[1][0].tolist()
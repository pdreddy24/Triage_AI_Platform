from sklearn.metrics import roc_auc_score, f1_score


def compute_metrics(y_true, y_pred):
    return {
        "auc": roc_auc_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred > 0.5)
    }
from services.scoring_service.model_loader import load_model, predict_proba


def test_model_prediction_range():
    load_model()

    features = [100, 0, 0, 0, 0, 0]
    prob = predict_proba(features)

    assert 0 <= prob <= 1
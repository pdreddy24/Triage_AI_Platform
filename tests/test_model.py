from services.scoring_service.feature_service import build_features


def test_feature_vector_shape():
    tx = {
        "transaction_id": "t1",
        "user_id": 1,
        "device_id": 1,
        "merchant_id": 10,
        "amount": 200
    }

    vector, features, velocity = build_features(tx)

    assert len(vector) == 6
    assert velocity >= 0
    assert all(isinstance(x, (int, float)) for x in vector)
from unittest.mock import patch, MagicMock


def test_full_pipeline(client):

    mock_scoring_response = {
        "transaction_id": "e2e-test",
        "timestamp": "2026-01-01T10:00:00",
        "risk_score": 0.25,
        "decision": "APPROVE",
        "velocity_1h": 0,
        "features_used": {},
        "model_version": "1.0.0"
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_scoring_response

    # 🔥 This now matches api.main exactly
    with patch("api.main.httpx.post") as mock_post:

        mock_post.return_value = mock_response

        # Login
        login_response = client.post("/login")
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Score transaction
        response = client.post(
            "/api/score",
            json={
                "transaction_id": "e2e-test",
                "user_id": 1,
                "device_id": 1,
                "merchant_id": 10,
                "amount": 300,
                "timestamp": "2026-01-01T10:00:00"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200

        data = response.json()
        assert data["decision"] == "APPROVE"
        assert data["risk_score"] == 0.25
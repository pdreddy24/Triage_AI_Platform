import pytest
from api.schemas import TransactionRequest
from datetime import datetime


def test_valid_transaction():
    tx = TransactionRequest(
        transaction_id="t1",
        user_id=1,
        device_id=1,
        merchant_id=10,
        amount=100,
        timestamp=datetime.now()
    )
    assert tx.amount == 100


def test_negative_amount():
    with pytest.raises(Exception):
        TransactionRequest(
            transaction_id="t2",
            user_id=1,
            device_id=1,
            merchant_id=10,
            amount=-50,
            timestamp=datetime.now()
        )
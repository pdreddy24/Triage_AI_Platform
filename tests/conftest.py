import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.alerts.models import Base
from api.alerts.repository import engine


@pytest.fixture(scope="module")
def client():
    #  Drop and recreate tables before tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c

    # Clean up after tests
    Base.metadata.drop_all(bind=engine)
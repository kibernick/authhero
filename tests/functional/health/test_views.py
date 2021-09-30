import pytest

from authhero.factories import create_app
from authhero.settings import TestConfig


app = create_app(TestConfig)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    data = response.json
    assert data == "OK"

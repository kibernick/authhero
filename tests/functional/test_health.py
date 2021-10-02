from flask import url_for
import pytest


@pytest.mark.functional
def test_health_check(client):
    response = client.get(url_for("health_check"))
    data = response.json
    assert data == "OK"

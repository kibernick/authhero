import json

import pytest
from flask import url_for

from authhero.models import User

TEST_USER_PASS = "muaddib"


def _create_test_user(session):
    user = User(
        username="paulatreides",
        first_name="Paul",
        last_name="Atreides",
        password=TEST_USER_PASS,
    )
    session.add(user)
    session.commit()
    return user


@pytest.mark.functional
def test_login_ok(session, client):
    user = _create_test_user(session)
    response = client.post(
        url_for("auth_login"),
        data=json.dumps(
            {
                "username": user.username,
                "password": TEST_USER_PASS,
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert 'api_key' in response.json


@pytest.mark.functional
def test_login_wrong_password(session, client):
    user = _create_test_user(session)
    response = client.post(
        url_for("auth_login"),
        data=json.dumps(
            {
                "username": user.username,
                "password": "harkonen",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 403


@pytest.mark.functional
def test_login_not_found(session, client):
    response = client.post(
        url_for("auth_login"),
        data=json.dumps(
            {
                "username": "doesnotexist",
                "password": "harkonen",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 401


@pytest.mark.functional
@pytest.mark.parametrize(
    "request_data",
    [
        ({}),
        ({"username": "test"}),
        ({"password": "test"}),
    ],
)
def test_login_missing_credentials(client, request_data):
    response = client.post(
        url_for("auth_login"),
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400

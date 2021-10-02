import os
import sys

import pytest
from flask import Flask
from flask.testing import FlaskClient

# Add project to path, for faster TDD :)
# TODO: remove when implementing an actual CI/CD system.
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)
from authhero.factories import create_app
from authhero.models import db as _db
from authhero.settings import TestConfig


@pytest.fixture(scope="session")
def app(request) -> Flask:
    """A test session-wide `Flask` application, with a request context."""
    app = create_app(TestConfig)
    ctx = app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app: Flask, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Client for making requests against the test app."""
    with app.test_client() as client:
        yield client

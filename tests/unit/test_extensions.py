from unittest.mock import patch, MagicMock

from flask import request

from authhero import extensions
from authhero import models


class TestLoadUser:
    @patch("authhero.extensions.models")
    def test_active_user(self, mock_models, app):
        user_mock = MagicMock(models.User)
        user_mock.is_active = True
        mock_models.User.query.get.return_value = user_mock

        user = extensions.load_user(1)
        assert user is not None

    @patch("authhero.extensions.models")
    def test_inactive_user(self, mock_models, app):
        user_mock = MagicMock(models.User)
        user_mock.is_active = False
        mock_models.User.query.get.return_value = user_mock

        user = extensions.load_user(1)
        assert user is None

    @patch("authhero.extensions.models")
    def test_missing_user(self, mock_models, app):
        mock_models.User.query.get.return_value = None

        user = extensions.load_user(1)
        assert user is None


class TestLoadUserFromRequest:
    @patch("authhero.extensions.models")
    def test_happy_path(self, mock_models, app):
        mock_user = MagicMock(models.User)
        mock_user.is_active = True

        mock_api_key = MagicMock(models.ApiKey)
        mock_api_key.user = mock_user

        query_result = MagicMock()
        query_result.first.return_value = mock_api_key

        mock_models.ApiKey.query.filter_by.return_value = query_result

        mock_models.ApiKey.check_valid_key.return_value = True

        with app.test_request_context(headers={'X-API-KEY': 'spice'}):
            user = extensions.load_user_from_request(request)

            assert user is not None

    @patch("authhero.extensions.models")
    def test_missing_header(self, mock_models, app):
        with app.test_request_context():
            user = extensions.load_user_from_request(request)

            assert user is None

    @patch("authhero.extensions.models")
    def test_header_invalid(self, mock_models, app):
        mock_models.ApiKey.check_valid_key.return_value = False

        with app.test_request_context(headers={'X-API-KEY': 'spice'}):
            user = extensions.load_user_from_request(request)

            assert user is None

    @patch("authhero.extensions.models")
    def test_api_key_not_found(self, mock_models, app):
        query_result = MagicMock()
        query_result.first.return_value = None

        mock_models.ApiKey.query.filter_by.return_value = query_result

        mock_models.ApiKey.check_valid_key.return_value = True

        with app.test_request_context(headers={'X-API-KEY': 'spice'}):
            user = extensions.load_user_from_request(request)

            assert user is None

    @patch("authhero.extensions.models")
    def test_user_not_active(self, mock_models, app):
        mock_user = MagicMock(models.User)
        mock_user.is_active = False

        mock_api_key = MagicMock(models.ApiKey)
        mock_api_key.user = mock_user

        query_result = MagicMock()
        query_result.first.return_value = mock_api_key

        mock_models.ApiKey.query.filter_by.return_value = query_result

        mock_models.ApiKey.check_valid_key.return_value = True

        with app.test_request_context(headers={'X-API-KEY': 'spice'}):
            user = extensions.load_user_from_request(request)

            assert user is None

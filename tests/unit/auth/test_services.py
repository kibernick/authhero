from unittest.mock import patch, MagicMock

from authhero import models
from authhero.auth import services


class TestRegisterUser:
    @patch("authhero.auth.services.models")
    def test_happy_path(self, mock_models, app):
        mock_models.User.get_by_username.return_value = None
        mock_models.User.return_value = MagicMock(models.User)

        _, status = services.register_user(**{"username": "testuser"})

        assert status == 201

    @patch("authhero.auth.services.models")
    def test_username_taken(self, mock_models, app):
        mock_models.User.get_by_username.return_value = MagicMock(models.User)

        user, status = services.register_user(**{"username": "testuser"})

        assert user is None
        assert status == 400


class TestLoginUser:
    @patch("authhero.auth.services.models")
    def test_happy_path_with_api_keys(self, mock_models, app):
        mock_user = MagicMock(models.User)
        mock_api_key = MagicMock(models.ApiKey)
        mock_user.valid_api_keys.return_value = [mock_api_key]
        mock_user.is_correct_password.return_value = True

        mock_models.User.get_by_username.return_value = mock_user

        res, status = services.login_user(username="testuser", password="pass")

        assert res is not None
        assert "api_key" in res
        assert status == 200

    @patch("authhero.auth.services.models")
    def test_happy_path_without_api_keys(self, mock_models, app):
        mock_user = MagicMock(models.User)
        mock_user.valid_api_keys.return_value = []
        mock_user.is_correct_password.return_value = True

        mock_models.User.get_by_username.return_value = mock_user

        res, status = services.login_user(username="testuser", password="pass")

        assert res is not None
        assert "api_key" in res
        assert status == 200

    @patch("authhero.auth.services.models")
    def test_user_not_found(self, mock_models, app):
        mock_models.User.get_by_username.return_value = None

        _, status = services.login_user(username="testuser", password="pass")

        assert status == 401

    @patch("authhero.auth.services.models")
    def test_wrong_password(self, mock_models, app):
        mock_user = MagicMock(models.User)
        mock_user.is_correct_password.return_value = False

        mock_models.User.get_by_username.return_value = mock_user

        _, status = services.login_user(username="testuser", password="pass")

        assert status == 403


class TestLoginUser:
    @patch("authhero.auth.services.models")
    def test_happy_path(self, mock_models, app):
        query_result = MagicMock()

        mock_models.ApiKey.query.filter_by.return_value = query_result

        _, status = services.logout_user(MagicMock(models.User))

        query_result.update.assert_called_with({'is_valid': False})
        assert status == 200

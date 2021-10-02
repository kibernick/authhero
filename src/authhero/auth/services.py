from typing import Tuple, TypedDict

from authhero import models


def register_user(**kwargs) -> Tuple[models.User, int]:
    existing_user = models.User.get_by_username(username=kwargs["username"])
    if existing_user is not None:
        # TODO: make this check part of input validation
        return None, 400

    new_user = models.User(**kwargs)
    models.db.session.add(new_user)
    models.db.session.commit()

    return new_user, 201


class LoginResult(TypedDict, total=False):
    api_key: str
    message: str


def login_user(username, password) -> Tuple[LoginResult, int]:
    """Log a user in and provide an api_key."""
    user = models.User.get_by_username(username=username)
    if user is None:
        return LoginResult(message="User not found"), 401

    if user.is_correct_password(password):
        if api_keys := user.valid_api_keys():
            api_key = api_keys[0]
        else:
            api_key = models.ApiKey(user=user)
            models.db.session.add(api_key)
            models.db.session.commit()

        return (
            LoginResult(
                api_key=api_key.id.hex,
                message=f"Welcome, {user.username}!",
            ),
            200,
        )

    return LoginResult(message="Wrong username/password"), 403


class LogoutResult(TypedDict, total=False):
    message: str


def logout_user(user: models.User) -> Tuple[LogoutResult, int]:
    """Deactivate all user's active sessions."""
    if user is None:
        raise ValueError("User object must be present.")

    api_keys = models.ApiKey.query.filter_by(user_id=user.id, is_valid=True)
    rows_updated = api_keys.update({"is_valid": False})
    models.db.session.commit()

    return (
        f"User ({user.username}) logged out, {rows_updated} sessions deactivated.",
        200,
    )

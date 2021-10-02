from typing import Tuple

from authhero import models


def list_users(is_active=True):
    return models.User.query.filter_by(is_active=is_active).all()


def update_user(
    username: str, current_user: models.User, **kwargs
) -> Tuple[models.User, int]:
    target_user = models.User.get_by_username(username=username)
    if target_user is None:
        return None, 404
    if target_user != current_user:
        return None, 403

    # Assuming that we've already validated kwargs.
    for key, value in kwargs.items():
        if value is not None:
            setattr(target_user, key, value)

    models.db.session.add(target_user)
    models.db.session.commit()
    return target_user


def delete_user(username: str, current_user: models.User) -> int:
    target_user = models.User.get_by_username(username=username)
    if target_user is None:
        return 404
    if target_user != current_user:
        return 403

    target_user.is_active = False

    models.db.session.add(target_user)
    models.db.session.commit()

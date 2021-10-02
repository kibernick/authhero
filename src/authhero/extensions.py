from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from authhero import models
from authhero.auth.views import ns as auth
from authhero.health.views import ns as health
from authhero.users.views import ns as users


def _init_api() -> Api:
    api = Api(
        title="AuthHero API",
        version="0.1.0",
        description="A sample authentication service.",
    )
    api.add_namespace(health)
    api.add_namespace(users)
    api.add_namespace(auth)
    return api


## Callbacks for flask_login


def load_user_from_request(request):
    """Enable authentication with `api_key`."""
    header_token = request.headers.get("X-API-KEY")
    if header_token and models.ApiKey.check_valid_key(header_token):
        if api_key := models.ApiKey.query.filter_by(
            id=header_token, is_valid=True
        ).first():
            if api_key.user.is_active:
                return api_key.user
    return None


def load_user(user_id):
    user = models.User.query.get(user_id)
    if user and user.is_active:
        return user
    return None


def _init_login_manager() -> LoginManager:
    login_manager = LoginManager()
    login_manager.request_loader(load_user_from_request)
    login_manager.user_loader(load_user)
    return login_manager


def init_extensions(app):
    """Initialize extensions for the Flask app."""
    SQLAlchemy(app)
    Migrate(app, models.db)
    _init_login_manager().init_app(app)
    _init_api().init_app(app)

from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from authhero.models import db
from authhero.views.health import health
from authhero.views.users import api as users


def init_api():
    api = Api(
        title="AuthHero API",
        version="0.1.0",
        description="A sample authentication service.",
    )
    api.add_namespace(health)
    api.add_namespace(users)
    return api


def init_extensions(app):
    SQLAlchemy(app)
    Migrate(app, db)

    init_api().init_app(app)

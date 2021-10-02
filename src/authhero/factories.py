from flask import Flask

from authhero.extensions import init_extensions
from authhero.settings import Config


def create_app(config_object: Config) -> Flask:
    """An application factory: http://flask.pocoo.org/docs/patterns/appfactories/"""
    app = Flask(__name__)
    app.config.from_object(config_object)

    init_extensions(app)

    return app

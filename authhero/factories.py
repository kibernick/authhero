from flask import Flask

from authhero.api import api
from authhero.settings import Config


def create_app(config_object=Config):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)  # todo: make it work with pydantic?

    # app.register_blueprint(users)

    api.init_app(app)

    return app

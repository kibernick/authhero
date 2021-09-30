from flask import Flask

from authhero.extensions import init_extensions


def create_app(config_object):
    """An application factory: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)  # todo: make it work with pydantic?

    init_extensions(app)

    return app

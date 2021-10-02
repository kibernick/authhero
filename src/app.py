from authhero.factories import create_app
from authhero.settings import DevConfig

CONFIG = DevConfig

"""This Flask app is used to run a development server with:

FLASK_ENV=development flask run

(inside the `src` directory)
"""
app = create_app(CONFIG)

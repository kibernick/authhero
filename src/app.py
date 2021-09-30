from authhero.factories import create_app
from authhero.settings import DevConfig

CONFIG = DevConfig

app = create_app(CONFIG)

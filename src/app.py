from authhero.factories import create_app
from authhero.settings import Config

CONFIG = Config  #todo: DevConfig if flask.helpers.get_debug_flag() else ProdConfig

app = create_app(CONFIG)

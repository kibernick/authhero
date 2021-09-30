from flask_restx import Api

from authhero.apis.health import health

api = Api(
    title="AuthHero API",
    version="0.1.0",
    description="A sample authentication service.",
)
api.add_namespace(health)

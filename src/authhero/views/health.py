from flask_restx import Namespace, Resource

health = Namespace("health", description="Health check")


@health.route("")
class Health(Resource):
    def get(self):
        """A simple check that the app is running."""
        return "OK"

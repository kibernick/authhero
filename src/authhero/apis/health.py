from flask_restx import Namespace, Resource

health = Namespace("health", description="Health check")


@health.route("", endpoint="health")
class Health(Resource):
    @health.doc("health")
    def get(self):
        """A simple check that the app is running."""
        return "OK"

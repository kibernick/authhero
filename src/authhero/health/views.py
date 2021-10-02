from flask_restx import Namespace, Resource

ns = Namespace("health", description="Health check")


@ns.route("")
class Check(Resource):
    def get(self):
        """A simple check that the app is running."""
        return "OK"

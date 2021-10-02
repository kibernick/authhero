from flask_login import current_user, login_required
from flask_restx import Namespace, Resource, fields

from authhero import models

from . import forms, services

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY",
    },
}

ns = Namespace(
    "users",
    description="Users REST API",
    authorizations=authorizations,
    security="apikey",
)
user_fields = {
    "username": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "password": fields.String,
}
user_plain = ns.model(
    "User",
    {f: user_fields[f] for f in ("username", "first_name", "last_name")},
)
user_update = ns.model(
    "UserUpdate",
    {f: user_fields[f] for f in ("first_name", "last_name")},
)


@ns.route("")
class List(Resource):
    @ns.marshal_with(user_plain)
    @login_required
    @ns.doc(security="apikey")
    def get(self):
        """List all active users."""
        return services.list_users()


@ns.route("/<string:username>")
@ns.doc(params={"username": "Username to look up or modify"})
class Details(Resource):
    @ns.marshal_with(user_plain)
    @login_required
    @ns.doc(security="apikey")
    def get(self, username):
        """Get details on an active user."""
        return models.User.get_by_username(username=username)

    @ns.expect(user_update)
    @ns.marshal_with(user_plain)
    @login_required
    @ns.doc(security="apikey")
    def patch(self, username):
        """Update details of existing user. Can only update self for now."""
        args = forms.update_user.parse_args()
        return services.update_user(username, current_user, **args)

    @ns.marshal_with(user_plain)
    @login_required
    @ns.doc(security="apikey")
    def delete(self, username):
        """Delete a User. Can only delete self for now."""
        return None, services.delete_user(username, current_user)


@ns.route("/me")
class MyDetails(Resource):
    @ns.marshal_with(user_plain)
    @login_required
    @ns.doc(security="apikey")
    def get(self):
        """Helper endpoint to get details on the logged in user."""
        return current_user

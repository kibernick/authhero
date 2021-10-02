from flask_login import current_user, login_required
from flask_restx import Namespace, Resource

from authhero.users.views import authorizations, user_fields, user_plain

from . import forms, services

ns = Namespace(
    "auth",
    description="Authentication API",
    authorizations=authorizations,
    security="apikey",
)
user_register = ns.model(
    "RegisterUser",
    {f: user_fields[f] for f in ("username", "first_name", "last_name", "password")},
)
user_login = ns.model(
    "LoginUser",
    {f: user_fields[f] for f in ("username", "password")},
)


@ns.route("/register")
class Register(Resource):
    @ns.expect(user_register)
    @ns.marshal_with(user_plain)
    def post(self):
        """Register a new user."""
        args = forms.registration.parse_args()
        return services.register_user(**args)


@ns.route("/login")
class Login(Resource):
    @ns.expect(user_login)
    def post(self):
        """Authenticate a user with username and password and return an api_key"""
        args = forms.login.parse_args()
        return services.login_user(username=args.username, password=args.password)


@ns.route("/logout")
class Logout(Resource):
    @login_required
    @ns.doc(security="apikey")
    def post(self):
        """Log out the active user, ending all their active sessions"""
        return services.logout_user(user=current_user)

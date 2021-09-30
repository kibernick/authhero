from flask_restx import Namespace, Resource, fields

from authhero.models import User, db
from authhero.forms import create_user

api = Namespace("users", description="Our main Users API")
user_model = api.model(
    "User",
    {
        "username": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
    },
)


@api.route("")
class UserList(Resource):
    @api.marshal_with(user_model)
    def get(self):
        """List all users."""
        return User.query.all()

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def post(self):
        """Create a new user."""
        args = create_user.parse_args()
        user = User(**args)

        db.session.add(user)
        db.session.commit()
        return user, 201

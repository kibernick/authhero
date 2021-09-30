from flask_restx import reqparse

create_user = reqparse.RequestParser(bundle_errors=True)
create_user.add_argument("username", required=True)
create_user.add_argument("first_name")
create_user.add_argument("last_name")

from flask_restx import reqparse

update_user = reqparse.RequestParser(bundle_errors=True)
update_user.add_argument("first_name")
update_user.add_argument("last_name")

from flask_restx import reqparse

registration = reqparse.RequestParser(bundle_errors=True)
registration.add_argument("username", required=True)
registration.add_argument("first_name")
registration.add_argument("last_name")
registration.add_argument("password", required=True)


login = reqparse.RequestParser(bundle_errors=True)
login.add_argument("username", required=True)
login.add_argument("password", required=True)

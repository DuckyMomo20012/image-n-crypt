from flask_restx import Model, fields, reqparse

from src.api.v1.auth.views import ns_auth

responseLoginModel: Model = ns_auth.model(
    "ResponseLogin",
    {
        "user_id": fields.String(
            description="User id", example="628385eb1dc6fa1a0cd84c38"
        ),
        "access_token": fields.String(
            description="JWT access token",
            example="eyJ0eXAiOiJKV1Q...",
        ),
    },
)

registerFormParser: reqparse.RequestParser = ns_auth.parser()
registerFormParser.add_argument("username", location="form", required=True)
registerFormParser.add_argument("password", location="form", required=True)
registerFormParser.add_argument("publicKey", location="form", required=True)

loginFormParser: reqparse.RequestParser = ns_auth.parser()
loginFormParser.add_argument("username", location="form", required=True)
loginFormParser.add_argument("password", location="form", required=True)

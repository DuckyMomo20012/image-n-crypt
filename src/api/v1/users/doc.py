from flask_restx import Model, fields

from src.api.v1.users.views import ns_users

userModel: Model = ns_users.model(
    "User",
    {
        "public_key": fields.String(
            description="Public key of user", example="27977 9431"
        ),
        "user_id": fields.String(
            description="User id", example="628385eb1dc6fa1a0cd84c38"
        ),
        "user_name": fields.String(description="User name", example="admin"),
    },
)

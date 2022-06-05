from flask import Blueprint
from flask_restx import Api
from src.api.auth.views import ns_auth as auth_api
from src.api.users.views import ns_users as users_api


# JWT views need to be imported for app.py to work
from .auth.views import (
    user_identity_lookup,
    user_lookup_callback,
    check_if_token_is_revoked,
    revoked_token_handler,
)

blueprint = Blueprint("v1", __name__)
api = Api(blueprint, version="1.0", title="API", description="API for the application")
api.add_namespace(auth_api)
api.add_namespace(users_api)

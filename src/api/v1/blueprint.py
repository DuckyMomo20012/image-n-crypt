from flask import Blueprint
from flask_restx import Api

from src.api.v1.auth.views import ns_auth
from src.api.v1.users.views import ns_users

# JWT views need to be imported for app.py to work
from .jwt.views import (
    check_if_token_is_revoked,
    revoked_token_handler,
    user_identity_lookup,
    user_lookup_callback,
)

__all__ = [
    "check_if_token_is_revoked",
    "revoked_token_handler",
    "user_identity_lookup",
    "user_lookup_callback",
]

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    },
}

blueprint = Blueprint("v1", __name__)
api = Api(
    blueprint,
    version="1.0",
    title="Image-N-crypt",
    description="API documentation for Image-N-crypt server",
    contact="Duong Vinh",
    contact_email="tienvinh.duong4@gmail.com",
    contact_url="https://github.com/DuckyMomo20012",
    license="MIT",
    license_url="https://github.com/DuckyMomo20012/image-n-crypt/blob/main/LICENSE",
    default_mediatype="application/json",
    authorizations=authorizations,
)
api.add_namespace(ns_auth)
api.add_namespace(ns_users)

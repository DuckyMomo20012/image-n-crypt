from src.api.v1.blueprint import blueprint
from src.api.v1.blueprint import (
    user_identity_lookup,
    user_lookup_callback,
    check_if_token_is_revoked,
    revoked_token_handler,
)

v1_blueprint = blueprint

import json

from app import jwt
from src.api.v1.auth.service import getTokenBlocklistByJTI
from src.api.v1.users.service import getUserById


@jwt.user_identity_loader
def user_identity_lookup(user):
    # when JWT is created, "id" is passed in private claim: "sub", in payload
    # section of JWT.
    # Then when user_lookup_loader is called, in "jwt_data" we can access "id"
    # via "sub".

    # This function pass user (User object from model) to create JWT

    # See more in login function
    curUser = json.loads(user.to_json())
    return {"id": curUser["_id"]["$oid"]}


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # jwt_data = {'typ': 'JWT', 'alg': 'HS256'} {'fresh': False, 'iat':
    # 1641892386, 'jti': '88d6273b-be35-446d-af03-8efc417937d2', 'type':
    # 'access', 'sub': {'id': '61dd3db8507cf07e5da19fe6'}, 'nbf': 1641892386,
    # 'exp': 1641893286}

    # This function extract "id" claim from JWT token, then we can query "id" and return
    # current user
    # jwt_data["jti"] is kinda a jwt id?
    userId = jwt_data["sub"]["id"]
    user = getUserById(userId)
    if user:
        return user
    # If user may be deleted from db, then return None to indicate that an error
    # occurred loading the user
    return None


# This function is called whenever a valid JWT is used to access a protected
# route
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]

    token_in_db = getTokenBlocklistByJTI(jti)

    return token_in_db is not None


@jwt.revoked_token_loader
def revoked_token_handler(jwt_header, jwt_payload):
    return (
        {
            "message": "Token has been revoked",
        },
        401,
    )


@jwt.invalid_token_loader
def invalid_token_handler(reason):
    return (
        {
            "message": f"{reason}",
        },
        422,
    )

import json
from datetime import datetime, timezone

from flask import abort, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.security import check_password_hash, generate_password_hash

from app import jwt
from src.api.v1.auth.model import LoginForm, RegisterForm, TokenBlocklist
from src.api.v1.auth.service import getTokenBlocklistByJTI
from src.api.v1.users.model import User
from src.api.v1.users.service import getUserById, getUserByUserName
from src.utils import flatten

# Namespace will prepend all routes with /auth, E.g: /auth/login,
# /auth/register, /auth/logout
# You can name it like auth_api or auth_namespace
ns_auth = Namespace("auth", description="Authentication related operations")

# This is for documentation only
responseLoginModel = ns_auth.model(
    "ResponseLogin",
    {
        "user_id": fields.String(description="User id"),
        "access_token": fields.String(description="JWT access token"),
    },
)

registerFormParser = ns_auth.parser()
registerFormParser.add_argument("username", location="form", required=True)
registerFormParser.add_argument("password", location="form", required=True)
registerFormParser.add_argument("publicKey", location="form", required=True)

loginFormParser = ns_auth.parser()
loginFormParser.add_argument("username", location="form", required=True)
loginFormParser.add_argument("password", location="form", required=True)


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
    # jwt_data = {'typ': 'JWT', 'alg': 'HS256'} {'fresh': False, 'iat': 1641892386, 'jti':
    # '88d6273b-be35-446d-af03-8efc417937d2', 'type': 'access', 'sub': {'id':
    # '61dd3db8507cf07e5da19fe6'}, 'nbf': 1641892386, 'exp': 1641893286}

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


@ns_auth.route("/register")
class Register(Resource):
    @ns_auth.doc(description="Register a new user")
    @ns_auth.response(201, "Successfully registered")
    @ns_auth.expect(registerFormParser)
    def post(self):
        # pass request data to form
        form = RegisterForm()
        # Don't have to pass request.form or check POST request, because
        # validate_on_submit automatically do that
        if form.validate_on_submit():
            data = request.form
            # NOTE: the field we access MUST persist with the field. Otherwise, we
            # will get the 400 Bad request
            username = data["username"]
            password = data["password"]
            publicKey = data["publicKey"]
            userList = getUserByUserName(username)
            if userList:
                abort(409, description="Username already exists")

            user = User(
                username=username,
                password=generate_password_hash(password, "sha256"),
                publicKey=publicKey,
            )
            user.save()
            return (
                "",
                201,
            )

        if form.errors:
            errorMessage = ", ".join(flatten(form.errors))
            abort(422, description=errorMessage)


@ns_auth.route("/login")
class Login(Resource):
    @ns_auth.doc(description="Login")
    @ns_auth.response(200, "Successfully logged in", model=responseLoginModel)
    @ns_auth.expect(loginFormParser)
    def post(self):
        # pass request data to form
        form = LoginForm()

        # Don't have to pass request.form or check POST request, because
        # validate_on_submit automatically do that
        if form.validate_on_submit():
            data = request.form
            username = data["username"]
            password = data["password"]
            user = getUserByUserName(username)
            if not user:
                # Should return 404 instead
                abort(422, description="Username or password is invalid")

            # print(user.to_json())

            if check_password_hash(user.password, password):
                # We passed in a User object, this user will be handled in
                # user_identity_loader, in that function we only
                # use id to create JWT token
                access_token = create_access_token(identity=user)
                return (
                    {
                        "user_id": str(user.id),
                        "access_token": access_token,
                    },
                    200,
                )
            else:
                abort(422, description="Username or password is invalid")

        if form.errors:
            errorMessage = ", ".join(flatten(form.errors))
            abort(422, description=errorMessage)


@ns_auth.route("/logout")
@ns_auth.doc(security="apikey")
class Logout(Resource):
    @jwt_required()
    @ns_auth.doc(description="Logout")
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)

        tokenBlock = TokenBlocklist(jti=jti, created_at=now)
        tokenBlock.save()

        return (
            {
                "message": "User logged out",
            },
            200,
        )

from flask import request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import jwt, csrf
from src.api.v1.auth.model import LoginForm, RegisterForm, TokenBlocklist
from src.api.v1.users.model import User
from src.api.v1.users.service import getUserById, getUserByUserName
from src.api.v1.auth.service import getTokenBlocklistByJTI
from flask_restx import Resource, Namespace

from flask_wtf.csrf import generate_csrf
from src.utils import flatten
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import json
from datetime import timezone, datetime

# Namespace will prepend all routes with /auth, E.g: /auth/login,
# /auth/register, /auth/logout
# You can name it like auth_api or auth_namespace
ns_auth = Namespace("auth", description="Authentication related operations")


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
    return make_response(
        {"status": "error", "code": "401", "message": "Token has been revoked"}, 401
    )


@jwt.invalid_token_loader
def invalid_token_handler(reason):
    return make_response(
        {"status": "error", "code": "422", "message": f"{reason}"}, 422
    )


@ns_auth.route("/register")
class Register(Resource):
    @ns_auth.response(200, "Success")
    def get(self):
        # Don't have to call jsonify since we return a dict
        return make_response({"csrf_token": generate_csrf()}, 200)

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
                return make_response(
                    {
                        "status": "error",
                        "code": "409",
                        "message": "Username already exists",
                    },
                    409,
                )

            user = User(
                username=username,
                password=generate_password_hash(password, "sha256"),
                publicKey=publicKey,
            )
            user.save()
            return make_response("", 201)

        if form.errors:
            errorMessage = ", ".join(flatten(form.errors))
            return make_response(
                {"status": "error", "code": "422", "message": errorMessage}, 422
            )


@ns_auth.route("/login")
class Login(Resource):
    @ns_auth.response(200, "Success")
    def get(self):
        return make_response({"csrf_token": generate_csrf()}, 200)

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
                return make_response(
                    {
                        "status": "error",
                        "code": "422",
                        "message": "Username or password is invalid",
                    },
                    422,
                )

            # print(user.to_json())

            if check_password_hash(user.password, password):
                # We passed in a User object, this user will be handled in
                # user_identity_loader, in that function we only
                # use id to create JWT token
                access_token = create_access_token(identity=user)
                return make_response(
                    {"user_id": str(user.id), "access_token": access_token}, 200
                )
            else:
                return make_response(
                    {
                        "status": "error",
                        "code": "422",
                        "message": "Username or password is invalid",
                    },
                    422,
                )

        if form.errors:
            errorMessage = ", ".join(flatten(form.errors))
            return make_response(
                {"status": "error", "code": "422", "message": errorMessage}, 422
            )


@ns_auth.route("/logout")
class Logout(Resource):
    @csrf.exempt
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)

        tokenBlock = TokenBlocklist(jti=jti, created_at=now)
        tokenBlock.save()

        return make_response(
            {"status": "success", "code": "200", "data": "User logged out"}, 200
        )

from datetime import datetime, timezone

from flask import abort, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restx import Namespace, Resource
from werkzeug.security import check_password_hash, generate_password_hash

from src.api.v1.auth.model import LoginForm, RegisterForm, TokenBlocklist
from src.api.v1.users.model import User
from src.api.v1.users.service import getUserByUserName
from src.utils import flatten

# Namespace will prepend all routes with /auth, E.g: /auth/login,
# /auth/register, /auth/logout
# You can name it like auth_api or auth_namespace
ns_auth: Namespace = Namespace("auth", description="Authentication related operations")

from src.api.v1.auth.doc import (  # noqa
    loginFormParser,
    registerFormParser,
    responseLoginModel,
)


@ns_auth.route("/register")
@ns_auth.param(
    "publicKey",
    (
        "Generated public key from function `generateAndWriteKeyToFile` in"
        " `helpers.crypto.crypto.py`.\nE.g: `27977 9431`"
    ),
    _in="formData",
)
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

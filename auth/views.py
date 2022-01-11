from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, jwt, csrf
from auth.model import User, LoginForm, RegisterForm, TokenBlocklist
from auth.service import (
    getUserById,
    getUserByUserName,
    getTokenBlocklistByJTI,
    getFirstTokenBlockList,
)
from flask_wtf.csrf import generate_csrf
from helpers.utils import flatten
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import json
from datetime import timezone, datetime

# @login_manager.user_loader
# def load_user(user_id):
#     userDoc = getUserById(user_id)
#     if not userDoc:
#         return AnonymousUserMixin()

#     userObj = json.loads(userDoc.to_json())
#     # id field inherited from UserMixin class (from flask_login)
#     user = User(
#         id=userObj["_id"]["$oid"],
#         username=userObj["username"],
#         password=userObj["password"],
#     )
#     return user


# @login_manager.unauthorized_handler
# def unauthorized():
#     # If unauthorize then redirect to login
#     return jsonify(
#         {
#             "status": "Unauthorized",
#             "code": 401,
#             "message": "The request could not be authenticated",
#         }
#     )


@jwt.user_identity_loader
def user_identity_lookup(user):
    # when JWT is created, "id" is passed in private claim: "sub", in payload section.
    # Then when user_lookup_loader is called, in "jwt_data" we can access "id"
    # via "sub".
    curUser = json.loads(user.to_json())
    return {"id": curUser["_id"]["$oid"]}


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # {'typ': 'JWT', 'alg': 'HS256'} {'fresh': False, 'iat': 1641892386, 'jti':
    # '88d6273b-be35-446d-af03-8efc417937d2', 'type': 'access', 'sub': {'id':
    # '61dd3db8507cf07e5da19fe6'}, 'nbf': 1641892386, 'exp': 1641893286}

    # Extract "id" claim from JWT token, then we can query "id" and return
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

    checkEmptyDB = getFirstTokenBlockList()

    if not checkEmptyDB:
        return False

    token_in_db = getTokenBlocklistByJTI(jti)
    print("token_in_redis", token_in_db)
    return token_in_db is not None


@jwt.revoked_token_loader
def revoked_token_handler(jwt_header, jwt_payload):
    return make_response(
        {"status": "error", "code": "401", "message": "User is not authorized"}, 401
    )


@app.route("/register", methods=["GET", "POST"])
def register():
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
        users = getUserByUserName(username)
        if len(users) > 0:
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

    # Don't have to call jsonify since we return a dict
    return make_response({"csrf_token": generate_csrf()}, 200)


@app.route("/login", methods=["GET", "POST"])
def login():
    # pass request data to form
    form = LoginForm()

    # Don't have to pass request.form or check POST request, because
    # validate_on_submit automatically do that
    if form.validate_on_submit():
        data = request.form
        username = data["username"]
        password = data["password"]
        user = getUserByUserName(username).first()
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
            # login_user(user)
            # We passed in a User object, this user will be handled in
            # user_identity_loader, in that function we only
            # use id to create JWT token
            access_token = create_access_token(identity=user)
            return make_response({"access_token": access_token}, 200)
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

    return make_response({"csrf_token": generate_csrf()}, 200)


@app.route("/logout", methods=["POST"])
@csrf.exempt
# @login_required
@jwt_required()
def logout():
    # logout_user()
    jti = get_jwt()["jti"]
    print("jti", type(jti))
    now = datetime.now(timezone.utc)

    tokenBlock = TokenBlocklist(jti=jti, created_at=now)
    tokenBlock.save()

    return make_response({"status": "success", "code": "200", "data": "User logged out"}, 200)

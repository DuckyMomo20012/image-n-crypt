from flask import request, render_template, url_for, jsonify
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from app import app, login_manager, csrf
from auth.model import User, LoginForm, RegisterForm
from auth.service import getUserById, getUserByUserName
from flask_login import login_user, login_required, AnonymousUserMixin
import bcrypt
import json
from flask_wtf.csrf import generate_csrf
from helpers.utils import flatten


@login_manager.user_loader
def load_user(user_id):
    userDoc = getUserById(user_id)
    if not userDoc:
        return AnonymousUserMixin()

    userObj = json.loads(userDoc.to_json())
    # id field inherited from UserMixin class (from flask_login)
    user = User(
        id=userObj["_id"]["$oid"],
        username=userObj["username"],
        password=userObj["password"],
    )
    return user


@login_manager.unauthorized_handler
def unauthorized():
    # If unauthorize then redirect to login
    return jsonify({"status": "error", "message": "User is not authorized"})


@app.route("/api/register", methods=["GET", "POST"])
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
        password = data["password"].encode()
        publicKey = data["publicKey"]
        users = getUserByUserName(username)
        if len(users) > 0:
            return jsonify({"status": "error", "message": "Username already exists"})
        salt = bcrypt.gensalt(rounds=16)
        hashPassword = bcrypt.hashpw(password, salt)
        user = User(username=username, password=hashPassword, publicKey=publicKey)
        user.save()
        login_user(user)
        return jsonify(
            {
                "status": "success",
                "data": {"username": username, "public_key": publicKey},
            }
        )

    if form.errors:
        errorMessage = ", ".join(flatten(form.errors))
        return jsonify({"status": "error", "message": errorMessage})

    return jsonify({"status": "success", "csrf_token": generate_csrf()})


@app.route("/api/login", methods=["GET", "POST"])
def login():
    # pass request data to form
    form = LoginForm()

    # Don't have to pass request.form or check POST request, because
    # validate_on_submit automatically do that
    if form.validate_on_submit():
        data = request.form
        username = data["username"]
        password = data["password"].encode()
        user = getUserByUserName(username).first()
        if not user:
            return jsonify(
                {"status": "error", "message": "Username or password is invalid"}
            )
        # print(user.to_json())
        if bcrypt.checkpw(password, user.password.encode()):
            login_user(user)
            return jsonify(
                {
                    "status": "success",
                    "data": {"username": user.username, "public_key": user.publicKey},
                }
            )
        else:
            return jsonify(
                {"status": "error", "message": "Username or password is invalid"}
            )

    if form.errors:
        errorMessage = ", ".join(flatten(form.errors))
        return jsonify({"status": "error", "message": errorMessage})

    return jsonify({"status": "success", "csrf_token": generate_csrf()})


@app.route("/api/logout", methods=["POST"])
@csrf.exempt
@login_required
def logout():
    logout_user()
    return jsonify({"status": "success", "data": "User logged out"})

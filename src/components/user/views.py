from app import app
from flask import make_response
from flask_jwt_extended import jwt_required
from src.components.user.service import getUserById, getAllUsers
import json


@app.route("/api/v1/users", methods=["GET"])
# @login_required
@jwt_required()
def getAllUserInformation():
    users = getAllUsers()
    if users:
        data = []

        for user in users:
            userData = json.loads(user.to_json())
            content = {
                "user_id": userData["_id"]["$oid"],
                "user_name": userData["username"],
                "public_key": userData["publicKey"],
            }
            data.append(content)

        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": [*data],
            },
            200,
        )

    return make_response({"status": "success", "code": "200", "data": []}, 200)


@app.route("/api/v1/users/<string:userId>", methods=["GET"])
# @login_required
@jwt_required()
def getUserInfomation(userId):
    user = json.loads(getUserById(userId).to_json())
    if user:
        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": {
                    "user_id": user["_id"]["$oid"],
                    "user_name": user["username"],
                    "public_key": user["publicKey"],
                },
            },
            200,
        )

    return make_response(
        {"status": "error", "code": "404", "message": "User not found"}, 404
    )

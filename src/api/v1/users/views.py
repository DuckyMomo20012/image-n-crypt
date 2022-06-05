from flask import make_response
from flask_jwt_extended import jwt_required
from src.api.v1.users.service import getUserById, getAllUsers
import json
from flask_restx import Resource, Namespace

# You can name it like users_api or users_namespace
ns_users = Namespace("users", description="User related operations")


@ns_users.route("/")
class GetAllUserInformation(Resource):
    @jwt_required()
    def get(self):
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


@ns_users.route("/<string:userId>")
class GetUserInformation(Resource):
    @jwt_required()
    def get(self, userId):
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


from .images.views import *

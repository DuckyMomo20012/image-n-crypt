import json

from flask import abort, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from src.api.v1.users.service import getAllUsers, getUserById

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
                jsonify([*data]),
                200,
            )

        return make_response(
            jsonify([]),
            200,
        )


@ns_users.route("/<string:userId>")
class GetUserInformation(Resource):
    @jwt_required()
    def get(self, userId):
        user = json.loads(getUserById(userId).to_json())
        if user:
            return make_response(
                {
                    "user_id": user["_id"]["$oid"],
                    "user_name": user["username"],
                    "public_key": user["publicKey"],
                },
                200,
            )

        abort(404, description="User not found")


from .images.views import *

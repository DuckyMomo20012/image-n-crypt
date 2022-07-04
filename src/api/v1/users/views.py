import json

from flask import abort
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Namespace, Resource

from src.api.v1.users.service import getAllUsers, getUserById

# You can name it like users_api or users_namespace
ns_users: Namespace = Namespace("users", description="User related operations")

from src.api.v1.users.doc import userModel  # noqa


# NOTE: Can't use "make_response" with marshal_with
# NOTE: Custom dict don't need "jsonify"
@ns_users.route("")
@ns_users.doc(security="apikey", description="List all user information")
class GetAllUserInformation(Resource):
    @jwt_required()
    @ns_users.marshal_list_with(userModel, description="All user information")
    def get(self):
        users = getAllUsers()
        if users:
            data = []

            for user in users:
                userData = json.loads(user.to_json())
                content = {
                    "public_key": userData["publicKey"],
                    "user_id": userData["_id"]["$oid"],
                    "user_name": userData["username"],
                }
                data.append(content)

            return (
                [*data],
                200,
            )

        return (
            [],
            200,
        )


@ns_users.route("/<string:userId>")
@ns_users.doc(security="apikey", description="Get user information")
class GetUserInformation(Resource):
    @jwt_required()
    @ns_users.marshal_with(userModel, description="User information")
    def get(self, userId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        user = getUserById(userId)
        if user:
            user = json.loads(user.to_json())
            return (
                {
                    "public_key": user["publicKey"],
                    "user_id": user["_id"]["$oid"],
                    "user_name": user["username"],
                },
                200,
            )

        abort(404, description="User not found")


from .images.views import (  # noqa
    DownloadImageAll,
    EditImagePermission,
    ListAndUploadImage,
    ShareImage,
)

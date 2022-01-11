from app import app
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from auth.service import getUserById


@app.route("/api/v1/users/<int:userId>", methods=["GET"])
# @login_required
@jwt_required()
def getUserInfomation(userId):
    user = getUserById(userId)
    if user:
        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": {"user_name": user.username, "public_key": user.publicKey},
            },
            200,
        )

    return make_response(
        {"status": "error", "code": "404", "message": "User not found"}, 404
    )

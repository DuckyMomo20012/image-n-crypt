from app import app
from flask import request, jsonify, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from flask_wtf.csrf import generate_csrf
from upload_image.model import Image, ImageForm, ImagePermission
from upload_image.service import *
from helpers.utils import getRandomFileName, flatten
from os import path
import json

# from flask_login import current_user, login_required


@app.route("/api/v1/users/<string:userId>/images", methods=["GET"])
# @login_required
@jwt_required()
def listImage(userId):
    # current_user is User document returned from user_lookup_loader
    curUserId = str(current_user.id)

    if userId != curUserId:
        return make_response(
            {"status": "error", "code": "401", "message": "User is not authorized"}, 401
        )

    images = getAllImageByUserId(curUserId)
    if images:
        imageList = [(img.nameImg + img.extImg) for img in images]
        return make_response(
            {"status": "success", "code": "200", "data": imageList}, 200
        )

    return make_response({"status": "success", "code": "200", "data": []}, 200)


@app.route("/api/v1/users/<string:userId>/images/<string:fileName>", methods=["GET"])
# @login_required
@jwt_required()
def downloadImage(userId, fileName):
    curUserId = str(current_user.id)

    # FIXME: Only get permission, instead of image
    image = getImageByNameAndUserId(userId, fileName)

    # fileExt = getExtension(request)

    if image:
        imagePermit = getImagePermissionsByUserId(userId, fileName, curUserId)

        # XOR ?
        if (not imagePermit) == (userId != curUserId):
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )
        data_byte = image.dataImg.read().decode("ISO-8859-1")
        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": {
                    "img_name": image.nameImg + image.extImg,
                    "img_content": data_byte,
                    "quotient": image.quotientImg,
                },
            },
            200,
        )

    return make_response(
        {"status": "error", "code": "404", "message": "Image not found"}, 404
    )


@app.route("/api/v1/users/<string:userId>/images/data", methods=["GET"])
# @login_required
@jwt_required()
def downloadImageAll(userId):
    curUserId = str(current_user.id)

    if userId != curUserId:
        return make_response(
            {"status": "error", "code": "401", "message": "User is not authorized"}, 401
        )

    images = getAllImageByUserId(curUserId)

    if images:
        data = []
        for image in images:
            data_byte = image.dataImg.read().decode("ISO-8859-1")
            content = {
                "img_name": image.nameImg + image.extImg,
                "img_content": data_byte,
                "quotient": image.quotientImg,
            }
            data.append(content)

        return make_response({"status": "success", "code": "200", "data": [*data]}, 200)

    # Because images can be None if there is no image on database, so instead of
    # return an error, we return an empty array
    return make_response({"status": "success", "code": "200", "data": []}, 200)


@app.route("/api/v1/users/<string:userId>/images/upload", methods=["GET", "POST"])
# @login_required
@jwt_required()
def uploadImage(userId):
    curUserId = str(current_user.id)

    if userId != curUserId:
        return make_response(
            {"status": "error", "code": "401", "message": "User is not authorized"}, 401
        )

    # Because we pass file via files request, not from body
    form = ImageForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        data = request.form
        quotient = data["quotient"]

        file = form.imageFile.data
        filename = secure_filename(file.filename)

        fileSplitName, ext = path.splitext(filename)

        # Query to check duplicate file name
        imageList = getImageByNameAndUserId(curUserId, fileSplitName)

        if imageList:
            fileSplitName = getRandomFileName(fileSplitName)

        image = Image(
            userId=userId,
            nameImg=fileSplitName,
            dataImg=file,
            quotientImg=quotient,
            extImg=ext,
        )
        image.save()
        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": {"img_name": image.nameImg + image.extImg},
            },
            200,
        )

    if form.errors:
        errorMessage = ", ".join(flatten(form.errors))
        return make_response(
            {"status": "error", "code": "422", "message": errorMessage}, 422
        )

    return make_response({"csrf_token": generate_csrf()}, 200)


@app.route(
    "/api/v1/users/<string:userId>/images/<string:fileName>/delete",
    methods=["GET", "DELETE"],
)
# @login_required
@jwt_required()
def deleteImage(userId, fileName):
    if request.method == "DELETE":
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        # fileExt = getExtension(request)
        image = getImageByNameAndUserId(curUserId, fileName)

        if image:
            image.delete()
            return make_response("", 204)

        return make_response(
            {"status": "error", "code": "404", "message": "Image not found"}, 404
        )

    return make_response({"csrf_token": generate_csrf()}, 200)


@app.route(
    "/api/v1/users/<string:userId>/images/<string:fileName>/permissions/<string:userPermissionId>",
    methods=["GET", "PUT", "DELETE"],
)
@jwt_required()
def editImagePermission(userId, fileName, userPermissionId):
    curUserId = str(current_user.id)

    if userId != curUserId:
        return make_response(
            {"status": "error", "code": "401", "message": "User is not authorized"},
            401,
        )

    image = getImageByNameAndUserId(curUserId, fileName)

    if image:
        imageOnePermit = getOneImagePermissionByUserId(
            userId, fileName, userPermissionId
        )
        if not imageOnePermit:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Permission for User id not found",
                },
                404,
            )

        if request.method == "DELETE":
            deleteImagePermissionByUserId(userId, fileName, userPermissionId)
            # image.permissions.pop(index)
            image.reload()
            return make_response("", 204)
        if request.method == "GET":
            return make_response(
                {
                    "status": "success",
                    "code": "200",
                    "data": imageOnePermit,
                },
                200,
            )
        if request.method == "PUT":
            sharedUserRole = request.form["role"]
            editImageRolePermissionByUserId(
                userId, fileName, userPermissionId, sharedUserRole
            )
            image.reload()
            return make_response("", 204)

    return make_response(
        {
            "status": "error",
            "code": "404",
            "message": "Image not found",
        },
        404,
    )


@app.route(
    "/api/v1/users/<string:userId>/images/<string:fileName>/permissions",
    methods=["GET", "POST"],
)
@jwt_required()
def shareImage(userId, fileName):
    curUserId = str(current_user.id)

    if userId != curUserId:
        return make_response(
            {"status": "error", "code": "401", "message": "User is not authorized"},
            401,
        )

    image = getImageByNameAndUserId(curUserId, fileName)

    if image:
        if request.method == "POST":
            sharedUserId = request.form["user_id"]
            sharedUserRole = request.form["role"]
            imageOnePermit = getOneImagePermissionByUserId(
                userId, fileName, sharedUserId
            )
            print("imageOnePermit", imageOnePermit)

            # DB can find a permission has userId == curUserid
            if imageOnePermit:
                return make_response(
                    {
                        "status": "error",
                        "code": "409",
                        "message": "Permission user id is already exists",
                    },
                    409,
                )

            newPermission = ImagePermission(userId=sharedUserId, role=sharedUserRole)
            image.permissions.append(newPermission)
            image.save()
            return make_response("", 201)
        if request.method == "GET":
            return make_response(
                {
                    "status": "success",
                    "code": "200",
                    "data": {
                        "permissions": image.permissions,
                        "csrf_token": generate_csrf(),
                    },
                },
                200,
            )

    return make_response(
        {
            "status": "error",
            "code": "404",
            "message": "Image not found",
        }
    )

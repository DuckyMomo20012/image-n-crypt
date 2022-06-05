from app import images as localImage
from flask import request, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_jwt_extended import jwt_required, current_user
from src.api.v1.users.images.model import Image, ImageForm, ImagePermission
from src.api.v1.users.images.service import *
from src.utils import getRandomFileName, flatten
from os import path
from flask_restx import Resource

from src.api.v1.users.views import ns_users


@ns_users.route("/<string:userId>/images")
class ListImage(Resource):
    @jwt_required()
    def get(self, userId):
        # current_user is User document returned from user_lookup_loader
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        images = getAllImages(curUserId)
        if images:
            imageList = [(img.nameImg + img.extImg) for img in images]
            return make_response(
                {"status": "success", "code": "200", "data": imageList}, 200
            )

        return make_response({"status": "success", "code": "200", "data": []}, 200)


@ns_users.route("/<string:userId>/images/<string:fileName>")
class DownloadImage(Resource):
    @jwt_required()
    def get(self, userId, fileName):
        curUserId = str(current_user.id)

        image = getOneImage(userId, fileName)

        if image:
            imagePermit = getOneImagePermission(userId, fileName, curUserId)

            # XOR ?
            if (not imagePermit) == (userId != curUserId):
                return make_response(
                    {
                        "status": "error",
                        "code": "401",
                        "message": "User is not authorized",
                    },
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


@ns_users.route("/<string:userId>/images/download-all")
class DownloadImageAll(Resource):
    @jwt_required()
    def get(self, userId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        images = getAllImages(curUserId)

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

            return make_response(
                {"status": "success", "code": "200", "data": [*data]}, 200
            )

        # Because images can be None if there is no image on database, so instead of
        # return an error, we return an empty array
        return make_response({"status": "success", "code": "200", "data": []}, 200)


@ns_users.route("/<string:userId>/images")
class UploadImage(Resource):
    @jwt_required()
    def post(self, userId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
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
            imageList = getOneImage(curUserId, fileSplitName)

            if imageList:
                fileSplitName = getRandomFileName(fileSplitName)

            image = Image(
                userId=userId,
                nameImg=fileSplitName,
                dataImg=file,
                quotientImg=quotient,
                extImg=ext,
            )
            # Save locally
            localImage.save(request.files["imageFile"])
            # Save on Mongo
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


@ns_users.route("/<string:userId>/images/<string:fileName>")
class DeleteImage(Resource):
    @jwt_required()
    def delete(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        # fileExt = getExtension(request)
        image = getOneImage(curUserId, fileName)

        if image:
            image.delete()
            return make_response("", 204)

        return make_response(
            {"status": "error", "code": "404", "message": "Image not found"}, 404
        )


@ns_users.route(
    "/<string:userId>/images/<string:fileName>/permissions/<string:userPermissionId>"
)
class EditImagePermission(Resource):
    @jwt_required()
    def get(self, userId, fileName, userPermissionId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        imageOnePermit = getOneImagePermission(userId, fileName, userPermissionId)

        if not imageOnePermit:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Permission for User id not found",
                },
                404,
            )

        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": imageOnePermit,
            },
            200,
        )

    @jwt_required()
    def put(self, userId, fileName, userPermissionId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        imageOnePermit = getOneImagePermission(userId, fileName, userPermissionId)

        if not imageOnePermit:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Permission for User id not found",
                },
                404,
            )
        image = getOneImage(curUserId, fileName)
        if not image:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Image not found",
                },
                404,
            )
        sharedUserRole = request.form["role"]
        editOneImageRolePermission(userId, fileName, userPermissionId, sharedUserRole)
        image.reload()
        return make_response("", 204)

    @jwt_required()
    def delete(self, userId, fileName, userPermissionId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        imageOnePermit = getOneImagePermission(userId, fileName, userPermissionId)

        if not imageOnePermit:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Permission for User id not found",
                },
                404,
            )

        image = getOneImage(curUserId, fileName)
        if not image:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Image not found",
                },
                404,
            )
        deleteOneImagePermission(userId, fileName, userPermissionId)
        # image.permissions.pop(index)
        image.reload()
        return make_response("", 204)


@ns_users.route("/<string:userId>/images/<string:fileName>/permissions")
class ShareImage(Resource):
    @jwt_required()
    def get(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        image = getOneImage(curUserId, fileName)
        if not image:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Image not found",
                },
                404,
            )

        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": {
                    "permissions": image.permissions,
                },
            },
            200,
        )

    @jwt_required()
    def post(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            return make_response(
                {"status": "error", "code": "401", "message": "User is not authorized"},
                401,
            )

        image = getOneImage(curUserId, fileName)
        if not image:
            return make_response(
                {
                    "status": "error",
                    "code": "404",
                    "message": "Image not found",
                },
                404,
            )

        sharedUserId = request.form["user_id"]
        sharedUserRole = request.form["role"]
        imageOnePermit = getOneImagePermission(userId, fileName, sharedUserId)
        # DB can find a permission has userId == curUserId
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
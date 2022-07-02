import json
from os import path

from app import images as localImage
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Resource, fields
from src.api.v1.users.images.model import Image, ImageForm, ImagePermission
from src.api.v1.users.images.service import *
from src.api.v1.users.views import ns_users
from src.utils import flatten, getRandomFileName
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

imageModel = ns_users.model(
    "Image",
    {
        "img_content": fields.String,
        "img_name": fields.String,
        "quotient": fields.String,
    },
)

permissionModel = ns_users.model(
    "Permission",
    {
        "userId": fields.String,
        "role": fields.String,
    },
)


@ns_users.route("/<string:userId>/images")
@ns_users.doc(security="apikey")
class ListAndUploadImage(Resource):
    @jwt_required()
    def get(self, userId):
        # current_user is User document returned from user_lookup_loader
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        images = getAllImages(curUserId)
        if images:
            imageList = [(img.nameImg + img.extImg) for img in images]
            return (
                imageList,
                200,
            )

        return (
            [],
            200,
        )

    @jwt_required()
    def post(self, userId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

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
            return (
                {
                    "img_name": image.nameImg + image.extImg,
                },
                200,
            )

        if form.errors:
            errorMessage = ", ".join(flatten(form.errors))
            abort(422, description=errorMessage)


@ns_users.route("/<string:userId>/images/<string:fileName>")
@ns_users.doc(security="apikey")
class DownloadAndDeleteImage(Resource):
    @jwt_required()
    @ns_users.marshal_with(imageModel, description="Image file")
    def get(self, userId, fileName):
        curUserId = str(current_user.id)

        image = getOneImage(userId, fileName)

        if image:
            imagePermit = getOneImagePermission(userId, fileName, curUserId)

            # XOR ?
            if (not imagePermit) == (userId != curUserId):
                abort(401, description="User is not authorized")

            data_byte = image.dataImg.read().decode("ISO-8859-1")
            return (
                {
                    "img_name": image.nameImg + image.extImg,
                    "img_content": data_byte,
                    "quotient": image.quotientImg,
                },
                200,
            )

        abort(404, description="Image not found")

    @jwt_required()
    def delete(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        # fileExt = getExtension(request)
        image = getOneImage(curUserId, fileName)

        if image:
            image.delete()
            return ("", 204)

        abort(404, description="Image not found")


@ns_users.route("/<string:userId>/images/download-all")
@ns_users.doc(security="apikey")
class DownloadImageAll(Resource):
    @jwt_required()
    @ns_users.marshal_list_with(imageModel, description="List of image files")
    def get(self, userId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

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

            return (
                [*data],
                200,
            )

        # Because images can be None if there is no image on database, so instead of
        # return an error, we return an empty array
        return (
            [],
            200,
        )


@ns_users.route(
    "/<string:userId>/images/<string:fileName>/permissions/<string:userPermissionId>"
)
@ns_users.doc(security="apikey")
class EditImagePermission(Resource):
    @jwt_required()
    @ns_users.marshal_with(permissionModel, description="Permissions of image")
    def get(self, userId, fileName, userPermissionId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        imageOnePermit = getOneImagePermission(userId, fileName, userPermissionId)

        if not imageOnePermit:
            abort(404, description="Permission for User id not found")

        return (
            json.loads(imageOnePermit.to_json()),
            200,
        )

    @jwt_required()
    def put(self, userId, fileName, userPermissionId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        imageOnePermit = getOneImagePermission(userId, fileName, userPermissionId)

        if not imageOnePermit:
            abort(404, description="Permission for User id not found")

        image = getOneImage(curUserId, fileName)
        if not image:
            abort(404, description="Image not found")

        sharedUserRole = request.form["role"]
        editOneImageRolePermission(userId, fileName, userPermissionId, sharedUserRole)
        image.reload()
        return ("", 204)

    @jwt_required()
    def delete(self, userId, fileName, userPermissionId):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        imageOnePermit = getOneImagePermission(userId, fileName, userPermissionId)

        if not imageOnePermit:
            abort(404, description="Permission for User id not found")

        image = getOneImage(curUserId, fileName)
        if not image:
            abort(404, description="Image not found")

        deleteOneImagePermission(userId, fileName, userPermissionId)
        # image.permissions.pop(index)
        image.reload()
        return ("", 204)


@ns_users.route("/<string:userId>/images/<string:fileName>/permissions")
@ns_users.doc(security="apikey")
class ShareImage(Resource):
    @jwt_required()
    @ns_users.marshal_list_with(
        permissionModel, description="List of image permissions"
    )
    def get(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        image = getOneImage(curUserId, fileName)
        if not image:
            abort(404, description="Image not found")

        return (
            json.loads(image.to_json())["permissions"],
            200,
        )

    @jwt_required()
    def post(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        image = getOneImage(curUserId, fileName)
        if not image:
            abort(404, description="Image not found")

        sharedUserId = request.form["user_id"]
        sharedUserRole = request.form["role"]
        imageOnePermit = getOneImagePermission(userId, fileName, sharedUserId)
        # DB can find a permission has userId == curUserId
        if imageOnePermit:
            abort(409, description="Permission user id is already exists")

        newPermission = ImagePermission(userId=sharedUserId, role=sharedUserRole)
        image.permissions.append(newPermission)
        image.save()
        return make_response("", 201)

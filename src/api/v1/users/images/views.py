import json
from os import path

from flask import abort, request
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Resource, fields
from werkzeug.datastructures import CombinedMultiDict, FileStorage
from werkzeug.utils import secure_filename

from app import images as localImage
from src.api.v1.users.images.model import Image, ImageForm, ImagePermission
from src.api.v1.users.images.service import (
    deleteOneImagePermission,
    editOneImageRolePermission,
    getAllImages,
    getOneImage,
    getOneImagePermission,
)
from src.api.v1.users.views import ns_users
from src.utils import flatten, getRandomFileName

# This is for documentation only
responseListImageModel = ns_users.model(
    "ResponseListImage",
    {
        "img_name": fields.String(description="Image name"),
    },
)

imageModel = ns_users.model(
    "Image",
    {
        "img_content": fields.String(description="Image encrypted content"),
        "img_name": fields.String(description="Image name"),
        "quotient": fields.String(description="Quotient for encrypted content"),
    },
)


permissionModel = ns_users.model(
    "Permission",
    {
        "userId": fields.String(description="User id"),
        "role": fields.String(description="User role for this image"),
    },
)

uploadImageFormParser = ns_users.parser()
uploadImageFormParser.add_argument(
    "imageFile", location="files", type=FileStorage, required=True
)
uploadImageFormParser.add_argument("quotient", location="form", required=True)


shareImageFormParser = ns_users.parser()
shareImageFormParser.add_argument("user_id", location="form", required=True)
shareImageFormParser.add_argument("role", location="form", required=True)

editPermissionFormParser = shareImageFormParser.copy()
editPermissionFormParser.remove_argument("user_id")


@ns_users.route("/<string:userId>/images")
@ns_users.doc(security="apikey")
class ListAndUploadImage(Resource):
    @jwt_required()
    @ns_users.doc(description="List all images")
    @ns_users.marshal_list_with(
        responseListImageModel, description="List of image file names"
    )
    def get(self, userId):
        # current_user is User document returned from user_lookup_loader
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        images = getAllImages(curUserId)
        if images:
            imageList = [
                {
                    "img_name": (img.nameImg + img.extImg),
                }
                for img in images
            ]
            return (
                imageList,
                200,
            )

        return (
            [],
            200,
        )

    @jwt_required()
    @ns_users.doc(description="Upload image")
    @ns_users.response(200, "Successfully uploaded image")
    @ns_users.expect(uploadImageFormParser)
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
@ns_users.param("fileName", "File name without extension")
class DownloadAndDeleteImage(Resource):
    @jwt_required()
    @ns_users.doc(description="Download image")
    @ns_users.marshal_with(imageModel, description="Image file")
    @ns_users.param(
        "userId", "User ID or image owner user ID (if downloading shared image)"
    )
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
    @ns_users.doc(description="Delete image")
    @ns_users.response(204, "Successfully deleted image")
    def delete(self, userId, fileName):
        curUserId = str(current_user.id)

        if userId != curUserId:
            abort(401, description="User is not authorized")

        # fileExt = getExtension(request)
        image = getOneImage(curUserId, fileName)

        if image:
            image.delete()
            return (
                "",
                204,
            )

        abort(404, description="Image not found")


@ns_users.route("/<string:userId>/images/download-all")
@ns_users.doc(security="apikey")
class DownloadImageAll(Resource):
    @jwt_required()
    @ns_users.doc(description="Download all images")
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
@ns_users.param("fileName", "File name without extension")
class EditImagePermission(Resource):
    @jwt_required()
    @ns_users.doc(description="Get image permissions of one user")
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
    @ns_users.doc(description="Edit image permissions of one user")
    @ns_users.response(204, "Successfully edited image permissions")
    @ns_users.expect(editPermissionFormParser)
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
        return (
            "",
            204,
        )

    @jwt_required()
    @ns_users.doc(description="Delete image permissions of one user")
    @ns_users.response(204, "Successfully deleted image permissions")
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
        return (
            "",
            204,
        )


@ns_users.route("/<string:userId>/images/<string:fileName>/permissions")
@ns_users.doc(security="apikey")
@ns_users.param("fileName", "File name without extension")
class ShareImage(Resource):
    @jwt_required()
    @ns_users.doc(description="List of image permissions")
    @ns_users.marshal_list_with(
        permissionModel, description="List all image permissions"
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
    @ns_users.doc(description="Share image with other user")
    @ns_users.response(204, "Successfully shared image")
    @ns_users.expect(shareImageFormParser)
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
        return (
            "",
            201,
        )

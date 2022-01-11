from app import app
from flask import request, jsonify, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from flask_wtf.csrf import generate_csrf
from auth.service import getUserById
from upload_image.model import Image, ImageForm
from upload_image.service import getAllImageByUserId, getImageByNameAndUserId
from helpers.utils import getRandomFileName, flatten, getExtension

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
        imageList = [img.nameImg for img in images]
        return make_response(
            {"status": "success", "code": "200", "data": imageList}, 200
        )

    return make_response({"status": "success", "code": "200", "data": []}, 200)


@app.route("/api/v1/users/<string:userId>/images/<string:fileName>", methods=["GET"])
# @login_required
@jwt_required()
def downloadImage(userId, fileName):
    curUserId = str(current_user.id)

    if userId != curUserId:
        return make_response(
            {"status": "error", "code": "401", "message": "User is not authorized"}, 401
        )

    fileExt = getExtension(request)
    image = getImageByNameAndUserId(curUserId, fileName + fileExt)

    if image:
        data_byte = image.dataImg.read().decode("ISO-8859-1")
        return make_response(
            {
                "status": "success",
                "code": "200",
                "data": {
                    "img_name": image.nameImg,
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
                "img_name": image.nameImg,
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

        # Query to check duplicate file name
        imageList = getImageByNameAndUserId(curUserId, filename)

        if imageList:
            filename = getRandomFileName(filename)

        image = Image(
            userId=userId, nameImg=filename, dataImg=file, quotientImg=quotient
        )
        image.save()
        return make_response(
            {"status": "success", "code": "200", "data": {"img_name": image.nameImg}},
            200,
        )

    if form.errors:
        errorMessage = ", ".join(flatten(form.errors))
        return make_response(
            {"status": "error", "code": "422", "message": errorMessage}, 422
        )

    return make_response({"csrf_token": generate_csrf()}, 200)


@app.route(
    "/api/v1/users/<string:userId>/images/<string:fileName>/delete", methods=["GET", "DELETE"]
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

        fileExt = getExtension(request)
        image = getImageByNameAndUserId(curUserId, fileName + fileExt)

        if image:
            image.delete()
            return make_response("", 204)

        return make_response(
            {"status": "error", "code": "404", "message": "Image not found"}, 404
        )

    return make_response({"csrf_token": generate_csrf()}, 200)
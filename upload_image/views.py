from app import app
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_login import current_user, login_required
from flask_wtf.csrf import generate_csrf
from upload_image.model import Image, ImageForm
from upload_image.service import getImageById, getImageByNameAndUserId
from helpers.utils import getRandomFileName, flatten

@app.route("/api/image-list", methods=["GET"])
@login_required
def image_list():
    curUser = current_user.get_id()

    images = getImageById(curUser)
    if images:
        imageList = [img.nameImg for img in images]
        return jsonify({"status": "success", "data": imageList})

    return jsonify({"status": "success", "data": "No image on database"})


@app.route("/api/image-list/download/<string:fileName>", methods=["GET"])
@login_required
def image_download(fileName):
    curUser = current_user.get_id()
    if not curUser:
        return jsonify({"status": "error", "message": "Image not found"})

    image = getImageByNameAndUserId(curUser, fileName)

    if image:
        data_byte = image.dataImg.read().decode("ISO-8859-1")
        return jsonify(
            {
                "status": "success",
                "data": {
                    "img_name": image.nameImg,
                    "img_content": data_byte,
                },
            }
        )

    return jsonify({"status": "error", "message": "Image not found"})


@app.route("/api/upload-image", methods=["GET", "POST"])
@login_required
def uploadImage():
    # Because we pass file via files request, not from body
    form = ImageForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        file = form.imageFile.data
        filename = secure_filename(file.filename)
        userId = current_user.get_id()

        # Query to check duplicate file name
        imageList = getImageByNameAndUserId(userId, filename)

        if imageList:
            filename = getRandomFileName(filename)

        image = Image(userId=userId, nameImg=filename, dataImg=file)
        image.save()
        return jsonify({"status": "success", "data": {"img_name": image.nameImg}})

    if form.errors:
        errorMessage = ", ".join(flatten(form.errors))
        return jsonify({"status": "error", "message": errorMessage})

    return jsonify({"csrf_token": generate_csrf()})

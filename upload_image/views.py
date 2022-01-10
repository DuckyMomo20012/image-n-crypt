from app import app
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_login import current_user, login_required
from flask_wtf.csrf import generate_csrf
from auth.service import getUserById
from upload_image.model import Image, ImageForm
from upload_image.service import getAllImageByUserId, getImageByNameAndUserId
from helpers.utils import getRandomFileName, flatten


@app.route("/api/image-list", methods=["GET"])
@login_required
def listImage():
    curUser = current_user.get_id()

    images = getAllImageByUserId(curUser)
    if images:
        imageList = [img.nameImg for img in images]
        return jsonify({"status": "success", "data": imageList})

    return jsonify({"status": "success", "data": "No image on database"})


@app.route("/api/download/<string:fileName>", methods=["GET"])
@login_required
def downloadImage(fileName):
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
                    "quotient" : image.quotientImg
                },
            }
        )

    return jsonify({"status": "error", "message": "Image not found"})


@app.route("/api/download-all", methods=["GET"])
@login_required
def downloadImageAll():
    curUser = current_user.get_id()
    if not curUser:
        return jsonify({"status": "error", "message": "Image not found"})

    images = getAllImageByUserId(curUser)

    if images:
        data = []
        for image in images:
            data_byte = image.dataImg.read().decode("ISO-8859-1")
            content = {
                "img_name": image.nameImg,
                "img_content": data_byte,
                "quotient" : image.quotientImg
            }
            data.append(content)

        return jsonify({"status": "success", "data": [*data]})

    return jsonify({"status": "error", "message": "Image not found"})


@app.route("/api/upload-image", methods=["GET", "POST"])
@login_required
def uploadImage():
    # Because we pass file via files request, not from body
    form = ImageForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        data = request.form
        quotient = data['quotient']

        file = form.imageFile.data
        filename = secure_filename(file.filename)
        userId = current_user.get_id()

        # Query to check duplicate file name
        imageList = getImageByNameAndUserId(userId, filename)

        if imageList:
            filename = getRandomFileName(filename)

        image = Image(userId=userId, nameImg=filename, dataImg=file, quotientImg=quotient)
        image.save()
        return jsonify({"status": "success", "data": {"img_name": image.nameImg}})

    if form.errors:
        errorMessage = ", ".join(flatten(form.errors))
        return jsonify({"status": "error", "message": errorMessage})

    return jsonify({"status": "success", "csrf_token": generate_csrf()})


@app.route("/api/delete/<string:fileName>", methods=["GET", "POST"])
@login_required
def deleteImage(fileName):

	if request.method == "POST":
		curUser = current_user.get_id()
		if not curUser:
			return jsonify({"status": "error", "message": "User not found"})

		image = getImageByNameAndUserId(curUser, fileName)

		if image:

			image.delete()

			return jsonify({"status": "success", "data": "Image deleted"})

		if not image:
			return jsonify({"status": "error", "message": "Image not found"})

		return jsonify({"status": "success", "csrf_token": generate_csrf()})

@app.route("/api/public-key", methods=["GET"])
@login_required
def getPublicKey():
    curUser = current_user.get_id()
    if not curUser:
        return jsonify({"status": "error", "message": "User not found"})

    user = getUserById(curUser)

    publicKey = user.publicKey

    return jsonify({"status": "success", "public_key": publicKey})
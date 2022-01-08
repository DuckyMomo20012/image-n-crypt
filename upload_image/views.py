from flask.helpers import url_for
from flask.templating import render_template
from flask_login.utils import login_required
from werkzeug.utils import redirect, secure_filename
from app import app
from flask_login import current_user
from upload_image.model import Image, ImageForm
from upload_image.service import getImageById

@app.route('/api/image-list')
@login_required
def image_list():
	curUser = current_user.get_id()

	images = getImageById(curUser)
	print("images", images)
	return 'image list'

@app.route('/api/upload-image', methods=['GET', 'POST'])
@login_required
def uploadImage():
	form = ImageForm()


	if form.validate_on_submit():
		file = form.imageFile.data
		filename = secure_filename(file.filename)
		userId = current_user.get_id()

		image = Image(userId=userId, nameImg=filename, dataImg=file)
		image.save()
	else:
		print(form.errors)


	return render_template('upload_image.html', form=form)


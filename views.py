from app import app
from auth.views import *
from upload_image.views import *


@app.route("/", methods = ['GET', 'POST'])
def index():
	return 'hello world';

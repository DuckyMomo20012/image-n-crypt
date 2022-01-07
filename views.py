from app import app
from auth.views import *


@app.route("/", methods = ['GET', 'POST'])
def index():
	return 'hello world';


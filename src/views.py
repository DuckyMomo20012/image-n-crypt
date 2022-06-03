from app import app
from src.api.auth.views import *
from src.api.upload_image.views import *
from src.api.user.views import *
from flask import render_template


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", context={"name": "Vinh"})

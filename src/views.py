from app import app
from src.components.auth.views import *
from src.components.upload_image.views import *
from src.components.user.views import *
from flask import render_template


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", context={"name": "Vinh"})

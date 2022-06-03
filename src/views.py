from app import app
from src.api import *
from flask import render_template


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", context={"name": "Vinh"})

from flask import Flask
from flask_mongoengine import MongoEngine

from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from flask_uploads import UploadSet, IMAGES, configure_uploads

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)


app.config.from_object("config.Config")
app.config.from_object("config.DBConfig")
app.config.from_object("config.JWTConfig")
# Kinda special, I currently can't set it in class 😐️
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

# UploadSet name is images so config -> UPLOADED_IMAGES_DEST
app.config["UPLOADED_IMAGES_DEST"] = "src/assets"

# 'IMAGES' for supporting multiple image format
# images = UploadSet("images", IMAGES)
# Currently, we only support png
images = UploadSet("images", ("png"))
configure_uploads(app, images)

# Auth using JWT
jwt = JWTManager(app)

# CSRF protection
csrf = CSRFProtect(app)

# DB
db = MongoEngine(app)

# Import both blueprints and jwt functions
from src.api import *

app.register_blueprint(v1_blueprint, url_prefix="/api/v1")

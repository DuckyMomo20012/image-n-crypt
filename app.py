from flask import Flask
from flask_mongoengine import MongoEngine

from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_uploads import UploadSet, IMAGES, configure_uploads
from environs import Env

env = Env()
# Read .env into os.environ
env.read_env()  # read .env file, if it exists

app = Flask(__name__)

app.config.update(
    # App configs
    SECRET_KEY=env.str("SECRET_KEY"),
    SESSION_COOKIE_SECURE=env.bool("SESSION_COOKIE_SECURE", default=False),
    UPLOADED_IMAGES_DEST=env.str("UPLOADED_IMAGES_DEST"),
    WTF_CSRF_ENABLED=env.bool("WTF_CSRF_ENABLED", default=False),
    FLASK_ENV=env.str("FLASK_ENV", default="production"),
    # JWT configs
    JWT_ACCESS_TOKEN_EXPIRES=env.int("JWT_ACCESS_TOKEN_EXPIRES", default=3600),
    JWT_SECRET_KEY=env.str("JWT_SECRET_KEY"),
    # MongoDB configs
    MONGODB_HOST=env.str("MONGODB_HOST"),
)

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

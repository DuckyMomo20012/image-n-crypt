from environs import Env
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_uploads import UploadSet, configure_uploads

env = Env()
# Read .env into os.environ
env.read_env()  # read .env file, if it exists

app = Flask(__name__)

app.config.update(
    # App configs
    SECRET_KEY=env.str("SECRET_KEY"),
    SESSION_COOKIE_SECURE=False,
    UPLOADED_IMAGES_DEST=env.str("UPLOADED_IMAGES_DEST"),
    WTF_CSRF_ENABLED=False,
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
configure_uploads(app, [images])

# Auth using JWT
jwt = JWTManager(app)

# DB
db = MongoEngine(app)

# Import both blueprints and jwt functions
from src.api import (  # noqa
    check_if_token_is_revoked,
    revoked_token_handler,
    user_identity_lookup,
    user_lookup_callback,
    v1_blueprint,
)

app.register_blueprint(v1_blueprint, url_prefix="/api/v1")

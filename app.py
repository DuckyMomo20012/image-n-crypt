from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
app.config.from_object("config.Config")
app.config.from_object("config.DBConfig")
app.config.from_object("config.JWTConfig")
# Kinda special, I currently can't set it in class :/
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
# configure_uploads(app, photos)

# Auth
# login_manager = LoginManager()
# login_manager.init_app(app)
jwt = JWTManager(app)

# CSRF protection: Can't make it works, I gave up
csrf = CSRFProtect(app)

# DB
db = MongoEngine(app)
from src.views import *

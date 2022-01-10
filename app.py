from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object("config.Config")
app.config.from_object("config.DBConfig")
# configure_uploads(app, photos)

# Auth
login_manager = LoginManager()

login_manager.init_app(app)

# CSRF protection: Can't make it works, I gave up
csrf = CSRFProtect(app)

# DB
db = MongoEngine(app)
from views import *

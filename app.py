from flask import Flask
from flask_mongoengine import MongoEngine
# from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object('config.Config')
# csrf = CSRFProtect(app)
db = MongoEngine(app)
from views import *

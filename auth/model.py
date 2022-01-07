import mongoengine as me
from flask_wtf import FlaskForm
import wtforms as wf
from wtforms.validators import DataRequired
from flask_login import UserMixin

class LoginForm(FlaskForm):
	username = wf.StringField(label='name')
	password = wf.StringField(label='password')

class User(me.Document, UserMixin):
	username = me.StringField()
	password = me.StringField()
	meta = {'collection': 'users'}

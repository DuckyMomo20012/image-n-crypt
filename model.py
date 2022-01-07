import mongoengine as me
from flask_wtf import FlaskForm
import wtforms as wf
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = wf.StringField(label='name')
	password = wf.StringField(label='password')

class User(me.Document):
	username = me.StringField()
	password = me.StringField()
	meta = {'collection': 'users'}

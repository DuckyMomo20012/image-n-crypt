import mongoengine as me
import wtforms as wf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

class ImageForm(FlaskForm):
	imageFile = FileField(label='image', validators=[FileRequired()])

class Image(me.Document):
	userId = me.StringField()
	nameImg = me.StringField()
	dataImg = me.ImageField()
	meta = {'collection': 'images'}

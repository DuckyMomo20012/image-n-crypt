import mongoengine as me
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ImageForm(FlaskForm):
    imageFile = FileField(
        label="image", validators=[FileRequired("Image file is required")]
    )


class Image(me.Document):
    userId = me.StringField()
    nameImg = me.StringField()
    dataImg = me.ImageField(size=(1024, 1024, True))
    meta = {"collection": "images"}

import mongoengine as me
import wtforms as wf
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.validators import DataRequired

from app import images


class ImageForm(FlaskForm):
    imageFile = FileField(
        label="image",
        validators=[
            FileRequired("Image file is required"),
            FileAllowed(images, "PNG images only!"),
        ],
    )
    quotient = wf.StringField(
        label="quotient", validators=[DataRequired("Quotient data is required")]
    )


class ImagePermission(me.EmbeddedDocument):
    userId = me.StringField()
    role = me.StringField()


class Image(me.Document):
    userId = me.StringField()
    nameImg = me.StringField()
    dataImg = me.ImageField()
    extImg = me.StringField()
    # Quotient for decryption
    quotientImg = me.StringField()
    permissions = me.EmbeddedDocumentListField(ImagePermission, default=[])
    meta = {"collection": "images"}

import mongoengine as me
import wtforms as wf
from bson.objectid import ObjectId
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


def validateObjectId(form, field):
    print(field.data)
    if not ObjectId.is_valid(field.data):
        raise wf.ValidationError(
            "Not a valid ObjectId, it must be a 12-byte input or a"
            " 24-character hex string"
        )


class ImagePermissionForm(FlaskForm):
    user_id = wf.StringField(
        label="userId",
        validators=[DataRequired("User id data is required"), validateObjectId],
    )
    role = wf.StringField(
        label="quotient",
        validators=[DataRequired("Quotient data is required")],
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

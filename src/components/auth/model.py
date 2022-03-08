import mongoengine as me
from flask_wtf import FlaskForm
import wtforms as wf
from wtforms.validators import DataRequired
from flask_login import UserMixin


class LoginForm(FlaskForm):
    username = wf.StringField(
        label="name", validators=[DataRequired("Username is required")]
    )
    password = wf.StringField(
        label="password", validators=[DataRequired("Password is required")]
    )


class RegisterForm(FlaskForm):
    username = wf.StringField(
        label="name", validators=[DataRequired("Username is required")]
    )
    password = wf.StringField(
        label="password", validators=[DataRequired("Password is required")]
    )
    publicKey = wf.StringField(
        label="public_key", validators=[DataRequired("Public key is required")]
    )

class TokenBlocklist(me.Document):
    jti = me.StringField()
    created_at = me.DateTimeField()
    meta = {"collections": "tokens"}
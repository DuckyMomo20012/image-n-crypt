import mongoengine as me
import wtforms as wf
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


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

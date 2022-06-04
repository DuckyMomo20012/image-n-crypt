import mongoengine as me

# from flask_login import UserMixin

# class User(me.Document, UserMixin):
class User(me.Document):
    username = me.StringField()
    password = me.StringField()
    publicKey = me.StringField()
    meta = {"collection": "users"}

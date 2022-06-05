import mongoengine as me


class User(me.Document):
    username = me.StringField()
    password = me.StringField()
    publicKey = me.StringField()
    meta = {"collection": "users"}

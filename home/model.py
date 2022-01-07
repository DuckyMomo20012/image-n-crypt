import mongoengine as me

class Image(me.Document):
	userId = me.StringField()
	imgContent = me.BinaryField()
	pass

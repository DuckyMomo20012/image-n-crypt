from auth.model import User, TokenBlocklist

def getUserByUserName(username):
	return User.objects(username=username).first()

def getUserById(id):
	# Find one
	return User.objects.get(id=id)

def getAllUsers():
    return User.objects()

def getTokenBlocklistByJTI(jti):
    return TokenBlocklist.objects(jti=jti).first()
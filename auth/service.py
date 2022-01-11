from auth.model import User, TokenBlocklist

def getUserByUserName(username):
	return User.objects(username=username)

def getUserById(id):
	# Find one
	return User.objects.get(id=id)

def getAllUsers():
    return User.objects()

def getFirstTokenBlockList():
    return TokenBlocklist.objects().first()

def getTokenBlocklistByJTI(jti):
    return TokenBlocklist.objects.get(jti=jti)
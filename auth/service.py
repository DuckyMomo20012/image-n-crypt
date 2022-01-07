from auth.model import User

def getUserByUserName(username):
	return User.objects(username=username)

def getUserById(id):
	# Find one
	return User.objects.get(id=id)

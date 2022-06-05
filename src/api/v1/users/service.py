from src.api.v1.users.model import User


def getUserByUserName(username):
    return User.objects(username=username).first()


def getUserById(id):
    # Find one
    return User.objects.get(id=id)


def getAllUsers():
    return User.objects()

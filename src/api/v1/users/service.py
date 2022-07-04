from bson.objectid import ObjectId

from src.api.v1.users.model import User


def getUserByUserName(username):
    return User.objects(username=username).first()


def getUserById(id):
    # Find one
    if not ObjectId.is_valid(id):
        return None

    return User.objects(id=id).first()


def getAllUsers():
    return User.objects()

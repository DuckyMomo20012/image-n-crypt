from bson.objectid import ObjectId
from mongoengine.queryset.visitor import Q

from src.api.v1.users.images.model import Image


def getAllImages(id):
    if not ObjectId.is_valid(id):
        return None

    return Image.objects(userId=id)


def getOneImage(id, fileName):
    if not ObjectId.is_valid(id):
        return None

    return Image.objects(Q(userId=id) & Q(nameImg=fileName)).first()


def getOneImagePermission(id, fileName, shareId):
    if not ObjectId.is_valid(id):
        return None

    if not ObjectId.is_valid(shareId):
        return None

    image = Image.objects(Q(userId=id) & Q(nameImg=fileName)).first()
    if not image:
        return None
    for permit in image.permissions:
        if permit.userId == shareId:
            return permit

    return None


def deleteOneImagePermission(id, fileName, shareId):
    if not ObjectId.is_valid(id):
        return None

    if not ObjectId.is_valid(shareId):
        return None

    # We don't have to set "S" in update_one when pull items
    Image.objects(
        Q(userId=id) & Q(permissions__userId=shareId) & Q(nameImg=fileName)
    ).update_one(pull__permissions__userId=shareId)


def editOneImageRolePermission(id, fileName, shareId, role):
    if not ObjectId.is_valid(id):
        return None

    if not ObjectId.is_valid(shareId):
        return None

    # Use "S" in update_one, because we don't know the position in the list
    Image.objects(
        Q(userId=id) & Q(permissions__userId=shareId) & Q(nameImg=fileName)
    ).update_one(set__permissions__S__role=role)

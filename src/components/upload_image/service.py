from src.components.upload_image.model import Image
from mongoengine.queryset.visitor import Q


def getAllImageByUserId(id):
    return Image.objects(userId=id)


def getImageByNameAndUserId(id, fileName):
    return Image.objects(Q(userId=id) & Q(nameImg=fileName)).first()


def getImagePermissionsByUserId(id, fileName, shareId):
    return Image.objects.get(Q(userId=id) & Q(nameImg=fileName)).permissions


def getOneImagePermissionByUserId(id, fileName, shareId):
    for permit in Image.objects.get(Q(userId=id) & Q(nameImg=fileName)).permissions:
        if permit.userId == shareId:
            return permit

    return None


def deleteImagePermissionByUserId(id, fileName, shareId):
    # We don't have to set "S" when pull items
    Image.objects(
        Q(userId=id) & Q(permissions__userId=shareId) & Q(nameImg=fileName)
    ).update_one(pull__permissions__userId=shareId)


def editImageRolePermissionByUserId(id, fileName, shareId, role):
    # Use "S", because we don't know the position in the list
    Image.objects(
        Q(userId=id) & Q(permissions__userId=shareId) & Q(nameImg=fileName)
    ).update_one(set__permissions__S__role=role)

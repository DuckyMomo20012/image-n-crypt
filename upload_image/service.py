from upload_image.model import Image
from mongoengine.queryset.visitor import Q


def getAllImageByUserId(id):
    return Image.objects(userId=id)


def getImageByNameAndUserId(id, fileName):
    return Image.objects(Q(userId=id) & Q(nameImg=fileName)).first()

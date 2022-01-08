from upload_image.model import Image

def getImageById(id):
	return Image.objects(userId=id)

from os import path
from datetime import datetime
from mimetypes import guess_extension

def getRandomFileName(fileName):
	name, ext = path.splitext(fileName)
	return f"{name}_%s{ext}" % (datetime.now().strftime("%Y%m%d%H%M%S"))

def flatten(arrDict):
	return [item for sublist in arrDict.values() for item in sublist]

def getExtension(req):
    return guess_extension(req.headers['Content-type'].partition(';')[0].strip())
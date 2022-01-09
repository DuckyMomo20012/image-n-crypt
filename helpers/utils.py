from datetime import datetime
def getRandomFileName(fileName):
	return f"{fileName}_%s" % (datetime.now().strftime("%Y%m%d%H%M%S"))
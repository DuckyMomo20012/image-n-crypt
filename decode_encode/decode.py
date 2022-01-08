from cv2 import PyRotationWarper
from function_support import *

ima = cv2.imread("output.png")
if __name__ == "__main__":
    result = Decrypted("encrypted.txt","rsa.txt")
    cv2.imwrite('grayscale.jpg',result)
   
                          
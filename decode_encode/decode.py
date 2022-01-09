from cv2 import PyRotationWarper
from function_support import *

ima = cv2.imread("../output.png")
if __name__ == "__main__":
<<<<<<< Updated upstream
    result = Decrypted("encrypted.txt","rsa.txt")
    cv2.imwrite('grayscale.jpg',result)
   
                          
=======
    result = Decrypted("rsa.txt", "../output.png", "../output.png")
    # cv2.imwrite('grayscale.jpg',result)

>>>>>>> Stashed changes

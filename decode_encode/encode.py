from cv2 import PyRotationWarper
from function_support import *
import json

save_file = "Encrypt.png"
pathImage = "1.png"
quotient = "quotient.txt"
if __name__ == "__main__":
    result = Encrypted(pathImage, "rsa_pub.txt", save_file, quotient)
    cv2.imshow("image", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

from cv2 import PyRotationWarper
from function_support import *
import json

save_file = "Encrypt.png"
pathImage = "1.png"
quotient = "quotient.txt"
if __name__ == "__main__":
    result = Encrypted(pathImage=pathImage, path_pbKey="rsa_pub.txt", save_imageEncrypted=save_file, save_quotient=quotient)
    cv2.imshow("image", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

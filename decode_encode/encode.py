from cv2 import PyRotationWarper
from function_support import *
import json
binary_file = open("output.png", 'rb')
ima = binary_file.read()
binary_file.close()
if __name__ == "__main__":
<<<<<<< Updated upstream
    result = Encrypted(ima,"rsa_pub.txt") 
    print(result)        
                          
=======
    result = Encrypted("rsa_pub.txt", ima, '../output.png')
    print(result)
>>>>>>> Stashed changes

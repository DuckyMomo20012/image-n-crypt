from function_support import *

save_file = "Encrypt.png"
pathImage = "1.png"
quotient = "quotient.txt"
if __name__ == "__main__":
    result = Encrypted(
        imgPath=pathImage,
        publicKeyPath="rsa_pub.txt",
        imgEncryptedSaveDst=save_file,
        quotientSaveDst=quotient,
    )
    cv2.imshow("image", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import sys
from client.old_client import *
from client.helper import *

def mainMenu():
    print("___MENU___")
    print("1. Login")
    print("2. Register")
    print("3. Quit")
    option = int(input("Enter your option: "))
    while option != 0:
        if option == 1:
            ans = getInput("username", "password")
            res = login(username=ans["username"], password=ans["password"])
            handleRes(res, "Logged in successfully ")
            # print("Logged in successfully")
            optionLogin()
        elif option == 2:
            ans = getInput("username", "password")
            res = register(username=ans["username"], password=ans["password"])
            handleRes(res, "Sign up successfully ")
            mainMenu()
        elif option == 3:
            sys.exit()
        else:
            print("Invalid choice. Enter 1 - 3")
            mainMenu()
        # except ValueError:
        #     print("Invalid choice. Enter 1 - 3")


def optionLogin():
    print("____HOME___")
    print("1. List image")
    print("2. Upload image")
    print("3. Dowload all images")
    print("4. Get User information")
    print("5. Logout")
    option = int(input("Enter your option: "))
    while option != 0:
        try:
            if option == 1:
                res = listImage()
                handleRes(res, "Image list ")
                optionInOptionLogin()
            elif option == 2:
                ans = getInput("image_path")
                getUserInformation()
                res = uploadImage(ans["image_path"])
                handleRes(res, "Upload image: ")
                optionLogin()
            elif option == 3:
                ans = getInput("private key")
                res = downloadImageAll(ans["private key"])
                handleRes(res, "Image downloaded")
                optionLogin()
            elif option == 4:
                res = getUserInformation()
                handleRes(res, "Information: ")
                optionLogin()
            elif option == 5:
                res = logout()
                handleRes(res, "Logout successfully")
                mainMenu()
            else:
                print("Invalid choice. Enter 1 - 5")
                optionLogin()
        except ValueError:
            print("Invalid choice. Enter 1 - 5")


def back():
    enter = int(input("Can you back(0.No - 1.Yes)? "))
    while enter < 2:
        if enter == 0:
            sys.exit()
        elif enter == 1:
            optionLogin()


def optionInOptionLogin():
    print("____IMAGE PROCESING___")
    print("1. Dowload image")
    print("2. Delete images")
    print("3. Share images")
    print("4. Get share images")
    print("5. Back")
    option = int(input("Enter your option: "))
    while option != 0:
        try:
            if option == 1:
                ans = getInput("file name", "private key")
                res = downloadImage(ans["file name"], ans["private key"])
                handleRes(res, "Image downloaded")
                back()
            elif option == 2:
                ans = getInput("delete file name")
                res = deleteImage(ans["delete file name"])
                handleRes(res, "File deleted")
                back()
            elif option == 3:
                ans = getInput("file name", "user id to share", "role")
                res = shareImage(ans["file name"], ans["user id to share"], ans["role"])
                handleRes(res, "File shared")
                back()
            elif option == 4:
                ans = getInput("file name", "user id")
                res = getShareImage(ans["file name"], ans["user id"])
                handleRes(res, "File downloaded")
                back()
            elif option == 5:
                optionLogin()
            else:
                print("Invalid choice. Enter 1 - 5")
                optionInOptionLogin()
        except ValueError:
            print("Invalid choice. Enter 1 - 5")


if __name__ == "__main__":
    access_token = ""
    userId = ""
    userName = ""
    publicKey = ""
    userPermissionId = "61de3861c23524e8eadb17f1"
    mainMenu()

import sys
from client.api import *
from client.helpers import *


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
            result = handleRes(res, "Logged in successfully ")
            print(result)
            # print("Logged in successfully")
            if "error" in result.lower():
                mainMenu()
            optionLogin()
        elif option == 2:
            ans = getInput("username", "password")
            res = register(username=ans["username"], password=ans["password"])
            print(handleRes(res, "Sign up successfully "))
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
                print(handleRes(res, "Image list "))
                optionInOptionLogin()
            elif option == 2:
                ans = getInput("image_path")
                getUserInformation()
                res = uploadImage(ans["image_path"])
                print(handleRes(res, "Upload image: "))
                optionLogin()
            elif option == 3:
                ans = getInput("private key file")
                res = downloadImageAll(ans["private key file"])
                print(handleRes(res, "Image downloaded"))
                optionLogin()
            elif option == 4:
                res = getUserInformation()
                print(handleRes(res, "Information: "))
                optionLogin()
            elif option == 5:
                res = logout()
                print(handleRes(res, "Logout successfully "))
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
    print("____IMAGE PROCESSING___")
    print("1. Download image")
    print("2. Delete image")
    print("3. Share image")
    print("4. Get shared image information")
    print("5. Download shared images")
    print("6. Delete image permission")
    print("7. Edit image permission")
    print("8. Back")
    option = int(input("Enter your option: "))
    while option != 0:
        try:
            if option == 1:
                ans = getInput("file name", "private key file")
                res = downloadImage(ans["file name"], ans["private key file"])
                print(handleRes(res, "Image downloaded"))
                optionLogin()
            elif option == 2:
                ans = getInput("delete file name")
                res = deleteImage(ans["delete file name"])
                print(handleRes(res, "File deleted"))
                optionLogin()
            elif option == 3:
                ans = getInput("file name", "user id to share", "role")
                res = shareImage(ans["file name"], ans["user id to share"], ans["role"])
                print(handleRes(res, "File shared"))
                optionLogin()
            elif option == 4:
                ans = getInput("file name")
                res = getShareImageAllInfo(ans["file name"])
                print(handleRes(res, "Image permission(s) "))
                optionLogin()
            elif option == 5:
                ans = getInput("file name", "user share id")
                res = getShareImage(ans["file name"], ans["user share id"])
                print(handleRes(res, "File downloaded"))
                optionLogin()
            elif option == 6:
                ans = getInput("file name", "user id")
                res = deleteImagePermissions(ans["file name"], ans["user id"])
                print(handleRes(res, "Permission deleted"))
                optionLogin()
            elif option == 7:
                ans = getInput("file name", "user id", "role")
                res = editImagePermissions(
                    ans["file name"], ans["user id"], ans["role"]
                )
                print(handleRes(res, "Permission edited"))
                optionLogin()
            elif option == 8:
                optionLogin()
            else:
                print("Invalid choice. Enter 1 - 8")
                optionInOptionLogin()
        except ValueError:
            print("Invalid choice. Enter 1 - 8")


if __name__ == "__main__":
    access_token = ""
    userId = ""
    userName = ""
    publicKey = ""
    userPermissionId = "61de3861c23524e8eadb17f1"
    mainMenu()

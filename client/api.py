import json
from os import path
from typing import Tuple

import requests  # type: ignore

from src.helpers import crypto as Crypto

# NOTE: Each function MUST return a tuple[str, int]


# NOTE: Each form has its own cookie, so when we send a GET request to request a
# form to submit, we have to set cookie for POST request
def register(username, password) -> Tuple[str, int]:
    e, d, n = Crypto.generateAndWriteKeyToFile("", writeFile=True)

    register_p = requests.post(
        "http://localhost:5000/api/v1/auth/register",
        data={"username": username, "password": password, "publicKey": f"{n} {e}"},
    )
    # print("register_p", register_p.text)
    return register_p.text, register_p.status_code


# NOTE: Only login GET request have "Set-Cookie" header
def login(username, password) -> Tuple[str, int]:
    global access_token
    global userId

    # NOTE: When login, cookie will be reset
    login_p = requests.post(
        "http://localhost:5000/api/v1/auth/login",
        data={"username": username, "password": password},
    )

    data = json.loads(login_p.text)
    if set(["user_id", "access_token"]).issubset(data.keys()):
        access_token = data["access_token"]
        userId = data["user_id"]

    return login_p.text, login_p.status_code


def listImage() -> Tuple[str, int]:
    global access_token
    global userId
    list_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return list_img_g.text, list_img_g.status_code


# NOTE: When logout, cookie will be reset
# NOTE: I have turned off csrf protection for logout route, so we don't have to
# request a csrf key
def logout() -> Tuple[str, int]:
    global access_token
    logout_p = requests.post(
        "http://localhost:5000/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return logout_p.text, logout_p.status_code


def uploadImage(fileName) -> Tuple[str, int]:
    global access_token
    global userId
    global publicKey
    if publicKey == "":
        getUserInformation()
    n, e = map(int, publicKey.split(" "))

    # NOTE: "imageFile" is field from ImageForm class
    name, ext = path.splitext(fileName)
    fileName_encrypt = name + ext
    Crypto.encrypt(
        fileName,
        n=n,
        e=e,
        imgEncryptedSaveDst=fileName_encrypt,
        quotientSaveDst="quotient.txt",
    )
    q = open("quotient.txt", "r")
    quotient = q.read()
    q.close()
    with open(fileName_encrypt, "rb") as f:
        upload_img_p = requests.post(
            f"http://localhost:5000/api/v1/users/{userId}/images",
            # Please send a file with this format!
            files={"imageFile": f},
            data={"quotient": quotient},
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        return upload_img_p.text, upload_img_p.status_code


def downloadImage(downloadFile, privateKeyPath) -> Tuple[str, int]:
    global access_token
    global userId
    name, ext = path.splitext(downloadFile)
    downloadFile_d = name + ext
    download_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    if download_img_g.status_code != 200:
        return download_img_g.text, download_img_g.status_code

    data = json.loads(download_img_g.text)
    imgData = data["img_content"]
    imgName = data["img_name"]
    quotientData = data["quotient"]
    with open("quotient.txt", "w") as q:
        q.write(quotientData)
    with open(imgName, "wb") as f:
        f.write(imgData.encode("ISO-8859-1"))
    Crypto.decrypt(
        imgEncryptedPath=downloadFile,
        privateKeyPath=privateKeyPath,
        imgDecryptedSaveDst=downloadFile_d,
    )

    return "", download_img_g.status_code


def downloadImageAll(pathPrivateKey) -> Tuple[str, int]:
    global access_token
    global userId
    download_img_all_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/download-all",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    if download_img_all_g.status_code != 200:
        return download_img_all_g.text, download_img_all_g.status_code

    data = json.loads(download_img_all_g.text)
    imgData = data

    for image in imgData:
        imgName = image["img_name"]
        imgContent = image["img_content"]
        quotientData = image["quotient"]
        with open("quotient.txt", "w") as q:
            q.write(quotientData)
        with open(imgName, "wb") as f:
            f.write(imgContent.encode("ISO-8859-1"))
        Crypto.decrypt(
            imgEncryptedPath=imgName,
            privateKeyPath=pathPrivateKey,
            imgDecryptedSaveDst=imgName,
        )

    return "", download_img_all_g.status_code


def deleteImage(deleteFile) -> Tuple[str, int]:
    global access_token
    global userId
    name, ext = path.splitext(deleteFile)

    delete_img_d = requests.delete(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return delete_img_d.text, delete_img_d.status_code


def getUserInformation() -> Tuple[str, int]:
    global access_token
    global userId, userName, publicKey
    user_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    if user_info_g.status_code == 200:
        user_info_g_data = json.loads(user_info_g.text)
        userId = user_info_g_data["user_id"]
        userName = user_info_g_data["user_name"]
        publicKey = user_info_g_data["public_key"]

    return user_info_g.text, user_info_g.status_code


def getAllUserInformation() -> Tuple[str, int]:
    global access_token
    user_info_g = requests.get(
        "http://localhost:5000/api/v1/users",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return user_info_g.text, user_info_g.status_code


def getShareImageInfo(fileShare, sharedUserId) -> Tuple[str, int]:
    global access_token
    global userId

    name, ext = path.splitext(fileShare)
    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",  # noqa
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    return permission_info_g.text, permission_info_g.status_code


def getShareImageAllInfo(fileShare) -> Tuple[str, int]:
    global access_token
    global userId

    name, ext = path.splitext(fileShare)

    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return permission_info_g.text, permission_info_g.status_code


def shareImage(fileShare, userPermission, role) -> Tuple[str, int]:
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # userPermission = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_p = requests.post(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        data={"user_id": userPermission, "role": role},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    return permission_info_p.text, permission_info_p.status_code


def editImagePermissions(fileShare, sharedUserId, role) -> Tuple[str, int]:
    global access_token
    global userId

    name, ext = path.splitext(fileShare)

    permission_info_p = requests.put(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",  # noqa
        data={"role": role},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    return permission_info_p.text, permission_info_p.status_code


def deleteImagePermissions(fileShare, sharedUserId) -> Tuple[str, int]:
    global access_token
    global userId

    name, ext = path.splitext(fileShare)

    permission_info_d = requests.delete(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",  # noqa
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return permission_info_d.text, permission_info_d.status_code


def getShareImage(downloadFile, sharedUserId) -> Tuple[str, int]:
    global access_token
    global userId
    name, ext = path.splitext(downloadFile)
    download_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{sharedUserId}/images/{name}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    if download_img_g.status_code != 200:
        return download_img_g.text, download_img_g.status_code

    data = json.loads(download_img_g.text)
    imgData = data["img_content"]
    imgName = data["img_name"]
    quotientData = data["quotient"]
    with open("quotient.txt", "w") as q:
        q.write(quotientData)
    with open(imgName, "wb") as f:
        f.write(imgData.encode("ISO-8859-1"))

    # Since the db didn't store the private, so the file can only be downloaded
    return "", download_img_g.status_code


__all__ = [
    "register",
    "login",
    "listImage",
    "logout",
    "uploadImage",
    "downloadImage",
    "downloadImageAll",
    "deleteImage",
    "getUserInformation",
    "getAllUserInformation",
    "getShareImageInfo",
    "getShareImageAllInfo",
    "shareImage",
    "editImagePermissions",
    "deleteImagePermissions",
    "getShareImage",
]

if __name__ == "__main__":
    access_token = ""
    userId = ""
    userName = ""
    publicKey = ""

    # GENERATE KEY

    # Crypto.create_write_key(dstPath="", writeFile=True)

    # USER INFORMATION

    # register(username="admin", password="admin")
    # logout()
    print(login(username="admin", password="admin"))
    print(getUserInformation())
    # print(getAllUserInformation())

    # CRUD IMAGE

    # print(listImage())
    # print(uploadImage(fileName="bicycle2.png"))
    # print(downloadImage(downloadFile="bicycle2.png", privateKeyPath="rsa_admin.txt"))
    # print(downloadImageAll(pathPrivateKey="rsa_admin.txt"))
    # print(deleteImage(deleteFile="bicycle2.png"))

    # CRUD IMAGE PERMISSIONS

    # print(shareImage("bicycle.png", "1234", "read"))
    # print(getShareImageInfo("bicycle.png", "1234"))
    # print(editImagePermissions("bicycle.png", "1234", "write"))
    # print(deleteImagePermissions("bicycle.png", "1234"))
    # print(getShareImageAllInfo("bicycle.png"))
    # print(getShareImage("bicycle.png", "628387db1dc6fa1a0cd84c42"))

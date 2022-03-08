import requests
import json
from src.components.decode_encode import function_support
from os import path

# RETURN a string for handleRes in helper.py handling

# 1. REGISTER:

# NOTE: Each form has its own cookie, so when we send a GET request to request a
# form to submit, we have to set cookie for POST request
def register(username, password):
    # global cookie
    register_g = requests.get("http://localhost:5000/register")
    register_data = json.loads(register_g.text)
    if "csrf_token" not in register_data.keys():
        return register_g.text
    csrfKey = register_data["csrf_token"]
    cookie = register_g.headers["Set-Cookie"]

    # print("register_g", register_g.text)

    e, d, n = function_support.create_write_key("", writeFile=True)

    register_p = requests.post(
        "http://localhost:5000/register",
        data={"username": username, "password": password, "publicKey": f"{n} {e}"},
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
        },
    )
    # print("register_p", register_p.text)
    return register_p.text


# GET - Success: {"csrf_token": "eyJ0eXAi..."}
# POST - Success: "", 201 - Created
# POST - Error: {"status": "error","code": "409","message": "Username already
# exists",},
# POST - Error: {"status": "error", "code": "422", "message": "Password is required, Public key is required"}


# 2. LOGIN:

# NOTE: Only login GET request have "Set-Cookie" header
def login(username, password):
    # global cookie
    global access_token
    global userId
    login_g = requests.get("http://localhost:5000/login")
    login_data = json.loads(login_g.text)
    if "csrf_token" not in login_data.keys():
        return login_g.text
    csrfKey = login_data["csrf_token"]
    cookie = login_g.headers["Set-Cookie"]

    # print("login_p", login_g.text)

    # NOTE: When login, cookie will be reset
    login_p = requests.post(
        "http://localhost:5000/login",
        data={"username": username, "password": password},
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
        },
    )
    # print("login_p", login_p.text)
    data = json.loads(login_p.text)
    if set(["user_id", "access_token"]).issubset(data.keys()):
        access_token = data["access_token"]
        userId = data["user_id"]
        # print("access_token", access_token)
        return str('{"data": {"user id": "%s"}}' % str(data["user_id"]))

    return login_p.text
    # cookie = login_p.headers["Set-cookie"]


# GET - Success: {"csrf_token": "eyJ0eXAi..."}
# POST - Success: {"access_token": "eyJ0eXAi...", "user_id": "61dea576762674330a3f17dc"}
# POST - Error: {"status": "error","code": "422","message": "Username or password is invalid",}
# POST - Error: {"status": "error", "code": "422", "message": "Password is required"}

# 3. LIST IMAGE:


def listImage():
    # global cookie
    global access_token
    global userId
    list_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    # print("list_img_g", list_img_g.text)
    return list_img_g.text


# GET - Success: {"status": "success", "code": "200", "data": ["traffic-sign.png","bicycle.png"]}
# GET - Success: {"status": "success", "code": "200", "data": []}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# GET - Error: {"status": "error", "code": "401", "message": "Token has been revoked"}

# 4. LOGOUT:

# NOTE: When logout, cookie will be reset
# NOTE: I have turned off csrf protection for logout route, so we don't have to
# request a csrf key
def logout():
    # global cookie
    global access_token
    logout_p = requests.post(
        "http://localhost:5000/logout",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    # print("logout", logout_p.text)
    return logout_p.text
    # cookie = logout_p.headers["Set-Cookie"]


# POST - Success: {"status": "success", "code": "200", "data": "User logged
# out"}
# POST - Error: {"status":"error", "code":"422", "message":"Bad Authorization
# header. Expected 'Authorization: Bearer <JWT>'"}

# 5. UPLOAD IMAGE:


def uploadImage(fileName):
    # global cookie
    global access_token
    global userId
    global publicKey
    if publicKey == "":
        getUserInformation()
    n, e = map(int, publicKey.split(" "))

    # NOTE: "imageFile" is field from ImageForm class
    # fileName = "bicycle2.png"
    name, ext = path.splitext(fileName)
    fileName_encrypt = name + "_e" + ext
    function_support.Encrypted(
        fileName,
        n=n,
        e=e,
        save_imageEncrypted=fileName_encrypt,
        save_quotient="quotient.txt",
    )
    q = open("quotient.txt", "r")
    quotient = q.read()
    q.close()
    with open(fileName_encrypt, "rb") as f:
        upload_img_p = requests.post(
            f"http://localhost:5000/api/v1/users/{userId}/images",
            files={"imageFile": f},
            data={"quotient": quotient},
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        # print("upload_img_p", upload_img_p.text)
        return upload_img_p.text


# POST - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# POST - Error: {"status": "error", "code": "401", "message": "Token has been revoked"}
# POST - Success:
# {"status": "success", "code": "200", "data": {"img_name": "bicycle.png_20220109213826"}}
# POST - Error: {"status": "error", "code": "422", "message": "Image file is required"}

# 6. DOWNLOAD IMAGE:


def downloadImage(downloadFile, privateKeyPath):
    # global cookie
    global access_token
    global userId
    # downloadFile = "bicycle2_e.png"
    name, ext = path.splitext(downloadFile)
    downloadFile_d = name + "_d" + ext
    download_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}",
        # headers={"Cookie": cookie},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    data = json.loads(download_img_g.text)
    if data["status"] == "error":
        return download_img_g.text
    imgData = data["data"]["img_content"]
    imgName = data["data"]["img_name"]
    quotientData = data["data"]["quotient"]
    with open("quotient.txt", "w") as q:
        q.write(quotientData)
    with open(imgName, "wb") as f:
        f.write(imgData.encode("ISO-8859-1"))
    function_support.Decrypted(
        path_ImageDecode=downloadFile,
        path_private_key=privateKeyPath,
        save_imageDecrypted=downloadFile_d,
    )


# GET - Success:
# {"status": "success","code": "200","data": {"img_name":
# "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",},}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# GET - Error: {"status": "error", "code": "401", "message": "Token has been
# revoked"}
# GET - Error: {"status": "error", "code": "404", "message": "Image not found"}

# 7. DOWNLOAD IMAGE ALL:


def downloadImageAll(pathPrivateKey):
    # global cookie
    global access_token
    global userId
    download_img_all_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/download-all",
        # headers={"Cookie": cookie},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    data = json.loads(download_img_all_g.text)
    if "data" not in data.keys():
        return download_img_all_g.text
    imgData = data["data"]

    for image in imgData:
        imgName = image["img_name"]
        imgContent = image["img_content"]
        quotientData = image["quotient"]
        with open("quotient.txt", "w") as q:
            q.write(quotientData)
        with open(imgName, "wb") as f:
            f.write(imgContent.encode("ISO-8859-1"))
        function_support.Decrypted(
            path_ImageDecode=imgName,
            path_private_key=pathPrivateKey,
            save_imageDecrypted=imgName,
        )


# GET - Success:
# {"status": "success","code": "200","data": [{"img_name":
# "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",}],}
# GET - Success:
# {"status": "success","code": "200","data": [],}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# GET - Error: {"status": "error", "code": "401", "message": "Token has been
# revoked"}


# 8. DELETE IMAGE:


def deleteImage(deleteFile):
    # global cookie
    global access_token
    global userId
    # deleteFile = "bicycle2_e.png"
    name, ext = path.splitext(deleteFile)

    delete_img_d = requests.delete(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    if delete_img_d.text:
        return delete_img_d.text
    # delete_img_d_data = json.loads(delete_img_d.text)
    # print("delete_img_p_data", delete_img_d_data)


# DELETE - Success: "", 204 - No Content
# DELETE - Error: {"status": "error", "code": "401", "message": "User is not authorized"}
# DELETE - Error: {"status": "error", "code": "404", "message": "Image not
# found"}
# DELETE - Error: {"status": "error", "code": "401", "message": "Token has been
# revoked"}

# 9. GET USER INFORMATION:


def getUserInformation():
    # global cookie
    global access_token
    global userId, userName, publicKey
    user_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}",
        headers={
            # "Cookie": cookie,
            "Authorization": f"Bearer {access_token}",
        },
    )

    user_info_g_data = json.loads(user_info_g.text)
    if user_info_g_data["status"] == "error":
        return user_info_g.text
    # print("public_key_g_data", user_info_g_data)
    userId = user_info_g_data["data"]["user_id"]
    userName = user_info_g_data["data"]["user_name"]
    publicKey = user_info_g_data["data"]["public_key"]
    return str(
        '{"data": {"user id": "%s", "userName": "%s", "publicKey": "%s"}}'
        % (str(userId), str(userName), str(publicKey))
    )


# GET - Success: {"status": "success", "code": "200", "data": {"user_id":
# "a23415...", "user_name":"admin", "public_key": "118403 97093"}}
# GET - Error: {"status": "error", "code": "404", "message": "User not found"}
# GET - Error: {"status": "error", "code": "401", "message": "Token has been
# revoked"}


# 10. GET USER INFORMATION:


def getAllUserInformation():
    # global cookie
    global access_token
    user_info_g = requests.get(
        f"http://localhost:5000/api/v1/users",
        headers={
            # "Cookie": cookie,
            "Authorization": f"Bearer {access_token}",
        },
    )

    user_info_g_data = json.loads(user_info_g.text)
    # print("public_key_g_data", user_info_g_data)
    return user_info_g.text


# GET - Success: {"status": "success", "code": "200", "data": [{"user_id":
# "a23415...", "user_name":"admin", "public_key": "118403 97093"}]}
# GET - Success: {"status": "success", "code": "200", "data": []}
# GET - Error: {"status": "error", "code": "401", "message": "Token has been
# revoked"}

# 11. Share image:


def getShareImageInfo(fileShare, sharedUserId):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # sharedUserId = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)
    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    permission_info_g_data = json.loads(permission_info_g.text)
    # print("permission_info_g_data", permission_info_g_data)
    return permission_info_g.text


# GET - Success: {"status": "success", "code": "200", "data": {"userId":
# "61de598f170caaeac86ce44d", "role": "write"},}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# GET - Error: {"status": "error", "code": "404", "message": "Image not found",}
# GET - Error: {"status": "error", "code": "404", "message": "Permission for
# User id not found",}


def getShareImageAllInfo(fileShare):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    userPermission = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    permission_info_g_data = json.loads(permission_info_g.text)
    if permission_info_g_data["status"] == "error":
        return permission_info_g.text
    # print("permission_info_g_data", permission_info_g_data)
    # cookie = permission_info_g.headers["Set-Cookie"]
    # csrfKey = permission_info_g_data["csrf_token"]
    return str(
        '{"data": {"permissions": "%s"}}'
        % (str(permission_info_g_data["data"]["permissions"]))
    )


# GET - Success: {"status": "success", "code": "200", "data": {"permissions": [{"userId":
# "61de598f170caaeac86ce44d", "role": "write"}],}
# GET - Success: {"status": "success", "code": "200", "data": {"permissions": [],}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# GET - Error: {"status": "error", "code": "404", "message": "Image not found",}


def shareImage(fileShare, userPermission, role):
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
    if permission_info_p.text:
        permission_info_p_data = json.loads(permission_info_p.text)
    return permission_info_p.text
    # print("permission_info_g_data", permission_info_p_data)


# POST - Success: "", 201
# POST - Error: {"status": "error", "code": "409", "message": "Permission user
# id is already exists",}
# POST - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# POST - Error: {"status": "error", "code": "404", "message": "Image not found",}


def editImagePermissions(fileShare, sharedUserId, role):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # sharedUserId = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_p = requests.put(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",
        data={"role": role},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    if permission_info_p.text:
        return permission_info_p.text


# PUT - Success: "", 204
# PUT - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# PUT - Error: {"status": "error", "code": "404", "message": "Image not found",}
# PUT - Error: {"status": "error", "code": "404", "message": "Permission for
# User id not found",}


def deleteImagePermissions(fileShare, sharedUserId):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # sharedUserId = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_d = requests.delete(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    if permission_info_d.text:
        return permission_info_d.text


# DELETE - Success: "", 204
# DELETE - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# DELETE - Error: {"status": "error", "code": "404", "message": "Image not found",}
# DELETE - Error: {"status": "error", "code": "404", "message": "Permission for
# User id not found",}


def getShareImage(downloadFile, sharedUserId):
    # global cookie
    global access_token
    global userId
    # downloadFile = "bicycle2_e.png"
    # sharedUserId = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(downloadFile)
    downloadFile_d = "bicycle_d.png"
    download_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{sharedUserId}/images/{name}",
        # headers={"Cookie": cookie},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    data = json.loads(download_img_g.text)
    if data["status"] == "error":
        return download_img_g.text
    imgData = data["data"]["img_content"]
    imgName = data["data"]["img_name"]
    quotientData = data["data"]["quotient"]
    with open("quotient.txt", "w") as q:
        q.write(quotientData)
    with open(imgName, "wb") as f:
        f.write(imgData.encode("ISO-8859-1"))

    # Since the db didn't store the private, so the file can only be downloaded

    # function_support.Decrypted(
    #     path_ImageDecode=downloadFile,
    #     path_private_key="rsa.txt",
    #     save_imageDecrypted=downloadFile_d,
    # )


# GET - Success:
# {"status": "success","code": "200","data": {"img_name":
# "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",},}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}
# GET - Error: {"status": "error", "code": "401", "message": "Token has been
# revoked"}
# GET - Error: {"status": "error", "code": "404", "message": "Image not found"}

if __name__ == "__main__":
    # cookie = ""
    access_token = ""
    userId = ""
    userName = ""
    publicKey = ""

    # GENERATE KEY

    # function_support.create_write_key(dstPath="", writeFile=True)

    # USER INFORMATION

    # register(username="admin", password="admin")
    # logout()
    login(username="admin", password="admin")
    # getUserInformation()
    # getAllUserInformation()

    # CRUD IMAGE

    # listImage()
    # uploadImage(fileName="bicycle2.png")
    # downloadImage(downloadFile="bicycle2_e.png", privateKeyPath="rsa.txt")
    # downloadImageAll(pathPrivateKey="rsa.txt")
    # deleteImage(deleteFile="bicycle2_e")

    # CRUD IMAGE PERMISSIONS

    # getShareImage("bicycle2_e.png", "61dea576762674330a3f17dc")
    # getShareImageInfo("bicycle2_e.png", "622725d4856271abe593a645")
    # shareImage("bicycle2_e.png", "622725d4856271abe593a645", "read")
    # deleteImagePermissions("bicycle2_e.png", "61de598f170caaeac86ce44d")
    # editImagePermissions("bicycle2_e.png", "61de598f170caaeac86ce44d", "write")
    # getShareImageAllInfo("bicycle2_e.png")

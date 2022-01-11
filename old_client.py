from PIL import Image
import requests
import json
from decode_encode import *
from decode_encode import function_support

# 1. REGISTER:

# NOTE: Each form has its own cookie, so when we send a GET request to request a
# form to submit, we have to set cookie for POST request
def register():
    # global cookie
    register_g = requests.get("http://localhost:5000/register")
    register_data = json.loads(register_g.text)
    csrfKey = register_data["csrf_token"]
    cookie = register_g.headers["Set-Cookie"]

    print("register_g", register_g.text)

    e, d, n = function_support.create_write_key("", writeFile=True)

    register_p = requests.post(
        "http://localhost:5000/register",
        data={"username": "admin", "password": "admin", "publicKey": f"{n} {e}"},
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
        },
    )
    print("register_p", register_p.text)


# GET - Success: {"csrf_token": "eyJ0eXAi...""}
# POST - Success: "", 201
# POST - Error: {"status": "error","code": "409","message": "Username already
# exists",},
# POST - Error: {"status": "error", "code": "422", "message": "Password is required, Public key is required"}


# 2. LOGIN:

# NOTE: Only login GET request have "Set-Cookie" header
def login():
    # global cookie
    global access_token
    login_g = requests.get("http://localhost:5000/login")
    login_data = json.loads(login_g.text)
    csrfKey = login_data["csrf_token"]
    cookie = login_g.headers["Set-Cookie"]

    print("login_p", login_g.text)

    # NOTE: When login, cookie will be reset
    login_p = requests.post(
        "http://localhost:5000/login",
        data={"username": "admin", "password": "admin"},
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
        },
    )
    print("login_p", login_p.text)
    data = json.loads(login_p.text)
    access_token = data["access_token"]
    print("access_token", access_token)
    # cookie = login_p.headers["Set-cookie"]


# GET - Success: {"csrf_token": "eyJ0eXAi...""}
# POST - Success: {"access_token": "eyJ0eXAi..."}
# POST - Error: {"status": "error","code": "422","message": "Username or password is invalid",}
# POST - Error: {"status": "error", "code": "422", "message": "Password is required"}

# 3. LIST IMAGE:


def listImage():
    # global cookie
    global access_token
    list_img_g = requests.get(
        "http://localhost:5000/api/v1/users/<int:userId>/images",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print("list_img_g", list_img_g.text)


# GET - Success: {"status": "success", "code": "200", "data": ["traffic-sign.png","bicycle.png"]}
# GET - Success: {"status": "success", "code": "200", "data": []}
# GET - Error: {"status": "error", "code": "401", "message": "User is not authorized"}

# 4. LOGOUT:

# NOTE: When logout, cookie will be reset
# NOTE: I have turned off csrf protection for logout route, so we don't have to
# request a csrf key
def logout():
    # global cookie
    logout_p = requests.post(
        "http://localhost:5000/api/logout",
        # headers={"Cookie": cookie},
    )
    print("logout", logout_p.text)
    cookie = logout_p.headers["Set-Cookie"]


# Success: {"data":"User logged out","status":"success"}
# NOTE: Unauthorized request will return this error
# Error: {"message":"User is not authorized","status":"error"}

# 5. UPLOAD IMAGE:


def uploadImage():
    # global cookie
    global access_token
    global userId, publicKey
    # public_key_g = requests.get(
    #     "http://localhost:5000/api/v1/users/<int:userId>/public-key",
    #     headers={"Cookie": cookie},
    # )
    # public_key_data = json.loads(public_key_g.text)
    # print("public_key_data", public_key_data)
    n, e = map(int, publicKey.split(" "))

    upload_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/upload",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    upload_img_data = json.loads(upload_img_g.text)
    csrfKey = upload_img_data["csrf_token"]

    print("upload_img_g", upload_img_g.text)

    # NOTE: "imageFile" is field from ImageForm class
    fileName = "bicycle2.png"
    fileName_encrypt = "bicycle2_e.png"
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
            f"http://localhost:5000/api/v1/users/{userId}/images/upload",
            files={"imageFile": f},
            data={"quotient": quotient},
            headers={
                "X-CSRFToken": csrfKey,
                # "Cookie": cookie,
                "Authorization": f"Bearer {access_token}",
            },
        )
        print("upload_img_p", upload_img_p.text)


# GET - Success: {"csrf_token": "eyJ0eXAi...""}
# GET - Error: {"status": "error", "code": "401", "message": "User is not authorized"}
# POST - Success:
# {"data":{"status": "success", "code": "200", "data": {"img_name": "bicycle.png_20220109213826"}}
# POST - Error: {"status": "error", "code": "422", "message": "Image file is required"}

# 6. DOWNLOAD IMAGE:


def downloadImage():
    # global cookie
    global access_token
    global userId
    downloadFile = "bicycle2_e.png"
    downloadFile_d = "bicycle_d.png"
    download_img_g = requests.get(
        f"http://127.0.0.1:5000//api/v1/users/{userId}/images/{downloadFile}",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = json.loads(download_img_g.text)
    imgData = data["data"]["img_content"]
    imgName = data["data"]["img_name"]
    quotientData = data["data"]["quotient"]
    with open("quotient.txt", "w") as q:
        q.write(quotientData)
    with open(imgName, "wb") as f:
        f.write(imgData.encode("ISO-8859-1"))
    function_support.Decrypted(
        path_ImageDecode=downloadFile,
        path_private_key="rsa.txt",
        save_imageDecrypted=downloadFile_d,
    )


# GET - Success:
# {"status": "success","code": "200","data": {"img_name":
# "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",},}
# GET - Error: {"status": "error", "code": "401", "message": "User is not authorized"}
# GET - Error: {"status": "error", "code": "404", "message": "Image not found"}

# 7. DOWNLOAD IMAGE ALL:


def downloadImageAll():
    # global cookie
    global access_token
    global userId
    download_img_all_g = requests.get(
        f"/api/v1/users/{userId}/images/data",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = json.loads(download_img_all_g.text)
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
            path_private_key="rsa.txt",
            save_imageDecrypted=imgName,
        )


# GET - Success:
# {"status": "success","code": "200","data": [{"img_name":
# "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",}],}
# GET - Success:
# {"status": "success","code": "200","data": [],}
# GET - Error: {"status": "error", "code": "401", "message": "User is not
# authorized"}


# 8. DELETE IMAGE:


def deleteImage():
    # global cookie
    global access_token
    global userId
    deleteFile = "bicycle2_e.png"
    # delete_img_g = requests.delete(
    #     f"/api/v1/users/{userId}/images/{deleteFile}",
    #     # headers={"Cookie": cookie}
    #     headers={"Authorization": f"Bearer {access_token}"},
    # )
    # delete_img_g_data = json.loads(delete_img_g.text)
    # print("delete_img_g_data", delete_img_g_data)
    # csrfKey = delete_img_g_data["csrf_token"]

    delete_img_p = requests.delete(
        f"/api/v1/users/{userId}/images/{deleteFile}",
        headers={
            # "X-CSRFToken": csrfKey,
            # "Cookie": cookie,
            "Authorization": f"Bearer {access_token}",
        },
    )
    delete_img_p_data = json.loads(delete_img_p.text)
    print("delete_img_p_data", delete_img_p_data)


# DELETE - Success: "", 201
# DELETE - Error: {"status": "error", "code": "401", "message": "User is not authorized"}
# DELETE - Error: {"status": "error", "code": "404", "message": "Image not found"}

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
    print("public_key_g_data", user_info_g_data)
    userId = user_info_g_data['user_id']
    userName = user_info_g_data['user_name']
    publicKey = user_info_g_data['public_key']

# GET - Success: {"status": "success", "code": "200", "data": {"user_id":
# "a23415...", "user_name":"admin", "public_key": "118403 97093"}}
# GET - Error: {"status": "error", "code": "404", "message": "User not found"}

if __name__ == "__main__":
    # cookie = ""
    access_token = ""
    userId = ""
    userName = ""
    publicKey = ""
    # register()
    login()
    listImage()
    # logout()
    # uploadImage()
    # downloadImage()
    # deleteImage()
    # getPublicKey()

# 1. Installation:

## 1.1. Install environment:

```console
python -m venv .venv
```

# 1.2. Activate environment:

```console
.venv\Scripts\activate
```

# 1.3. Install libs:

```console
pip install -r requirements.txt
```

# 1.4. Start app:

```console
flask run
```

# 2. REST API:

> At first, the server I built was based entirely on session cookie based
> authentication using "Flask-Login" library. But after a few researches, I switched to
> token based authentication with "Flask-JWT-Extended" library, which use JWT
> (JSON Web Token) to authenticate. So you may find some pieces of code that was
> use cookie I left behind.

## 2.0 REST API endpoints:

<table>
<tbody>
<tr>
<td> Method </td> <td> URL </td> <td> Description </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users </td> <td> Get all users information </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt </td> <td> Get user information </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images </td> <td> Get user all images </td>
</tr>
<tr>
<td> POST </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/upload </td> <td> Upload image </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/data </td> <td> Download all images </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt </td> <td> Download specific image </td>
</tr>
<tr>
<td> DELETE </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/delete </td> <td> Delete specific image </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions </td> <td> Get all image permissions </td>
</tr>
<tr>
<td> POST </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions </td> <td> Share image to specific user (Grant permission) </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td> <td> Get specific permission of image </td>
</tr>
<tr>
<td> PUT </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td> <td> Edit specific permission of image </td>
</tr>
<tr>
<td> DELETE </td> <td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td> <td> Delete specific permission of image </td>
</tr>
<tr>
<td> GET </td> <td> http://localhost:5000/api/v1/users/&ltstring:sharedUserId&gt/images/&ltstring:fileName&gt </td> <td> Download shared image (the same as download specific image) </td>
</tr>
</tbody>
</table>

## 2.1. Login:

> **⚠️ ⚠️ NOTE:** Whenever user login or logout, that means user's session is over,
> so cookie will be reset. Also, the JWT token will be sent to blacklist.

Currently when we login, the JWT token is stored on the client persistently ->
Vulnerable to CSRF & XSS attacks.

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/login </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "csrf_token": "eyJ0eXAi..." }
```

</td>
</tr>

<tr>
<td> POST </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "access_token": "eyJ0eXAi...", "user_id": "61dea576762674330a3f17dc" }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
# global cookie
global access_token
global userId
login_g = requests.get("http://localhost:5000/login")
login_data = json.loads(login_g.text)
csrfKey = login_data["csrf_token"]
cookie = login_g.headers["Set-Cookie"]
# print("login_p", login_g.text)
# ⚠️ NOTE: When login, cookie will be reset
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
if data:
    access_token = data["access_token"]
    userId = data["user_id"]
    # print("access_token", access_token)
    return str('{"data": {"user id": "%s"}}' % str(data["user_id"]))
# Reset cookie if you use flask-login for cookie based session
# cookie = login_p.headers["Set-cookie"]
```

</details>

## 2.2. Logout:

> ⚠️ NOTE: I have turned off CSRF protection for logout route, so we don't have to request a CSRF key.

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/logout </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> POST </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "status": "success", "code": "200", "data": "User logged out" }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
```

</details>

## 2.3. Register:

~~After register, user is logged in, so cookie is reset~~. User no longer login
after registration.

When logged in, public and private for RSA algorithm is created for user at current directory
(directory where client is running):

- Public key is save with file name: "rsa_pub.txt".

- Private key is save with file name: "rsa.txt". If the file name is already
  exists, then the file name will be append with the timestamp. E.g: rsa_20220112162809.txt

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/register </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "csrf_token": "eyJ0eXAi..." }
```

</td>
</tr>
<tr>
<td> POST </td> <td> Success </td> <td> 201 </td> <td> Created - No response </td>
</tr>
<tr>
<td> POST </td> <td> Error </td> <td> 409 </td>
<td>

```json
{ "status": "error", "code": "409", "message": "Username already exists" }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
# global cookie
register_g = requests.get("http://localhost:5000/register")
register_data = json.loads(register_g.text)
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
```

</details>

## 2.4. List images:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": ["traffic-sign.png", "bicycle.png"]
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "status": "success", "code": "200", "data": [] }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
```

</details>

## 2.5. Upload image:

> ⚠️ NOTE: Temporarily accepting .PNG image extension only.

When user upload a image (.png), the image is encrypted with public key and
return the encrypted image along with the "quotient.txt". The quotient later is
sent along with the image content.

Why there is a quotient file?

When encrypt the image with RSA algorithm, the image is broken and can't open.
Use quotient is use for modulo the encrypt message, so the image still can be
opened, but the opener may or may not understand the image.

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/upload </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "csrf_token": "eyJ0eXAi..." }
```

</td>
</tr>
<tr>
<td> POST </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": { "img_name": "bicycle.png_20220109213826" }
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
# global cookie
global access_token
global userId
global publicKey
# public_key_g = requests.get(
#     "http://localhost:5000/api/v1/users/<string:userId>/public-key",
#     headers={"Cookie": cookie},
# )
# public_key_data = json.loads(public_key_g.text)
# print("public_key_data", public_key_data)
if publicKey == "":
    getUserInformation()
n, e = map(int, publicKey.split(" "))
upload_img_g = requests.get(
    f"http://localhost:5000/api/v1/users/{userId}/images/upload",
    # headers={"Cookie": cookie},
    headers={"Authorization": f"Bearer {access_token}"},
)
upload_img_data = json.loads(upload_img_g.text)
csrfKey = upload_img_data["csrf_token"]
cookie = upload_img_g.headers["Set-Cookie"]
# print("upload_img_g", upload_img_g.text)
# ⚠️ NOTE: "imageFile" is field from ImageForm class
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
        f"http://localhost:5000/api/v1/users/{userId}/images/upload",
        files={"imageFile": f},
        data={"quotient": quotient},
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
            "Authorization": f"Bearer {access_token}",
        },
    )
    # print("upload_img_p", upload_img_p.text)
    return upload_img_p.text
```

</details>

## 2.6. Download image:

The URI should not have the file extension.

The file is downloaded then client use the private key from local and the
quotient content downloaded to decrypt the message

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": {
    "img_name": "bicycle.png",
    "img_content": "\u00ff...",
    "quotient": "22 22..."
  }
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{ "status": "error", "code": "404", "message": "Image not found" }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
```

</details>

## 2.7 Download ALL images:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/data </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": [
    {
      "img_name": "bicycle.png",
      "img_content": "\u00ff...",
      "quotient": "22 22..."
    }
  ]
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": []
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
def downloadImageAll(pathPrivateKey):
    # global cookie
    global access_token
    global userId
    download_img_all_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/data",
        # headers={"Cookie": cookie},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
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
            path_private_key=pathPrivateKey,
            save_imageDecrypted=imgName,
        )
```

</details>

## 2.8. Delete image:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/delete </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "csrf_token": "eyJ0eXAi..." }
```

</td>
</tr>
<tr>
<td> DELETE </td> <td> Success </td> <td> 204 </td> <td> No Content - No response </td>
</tr>
<tr>
<td> DELETE </td> <td> Error </td> <td> 404 </td>
<td>

```json
{ "status": "error", "code": "404", "message": "Image not found" }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
def deleteImage(deleteFile):
    # global cookie
    global access_token
    global userId
    # deleteFile = "bicycle2_e.png"
    name, ext = path.splitext(deleteFile)
    delete_img_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/delete",
        # headers={"Cookie": cookie}
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    delete_img_g_data = json.loads(delete_img_g.text)
    print("delete_img_g_data", delete_img_g_data)
    csrfKey = delete_img_g_data["csrf_token"]
    cookie = delete_img_g.headers["Set-Cookie"]

    delete_img_d = requests.delete(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/delete",
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
            "Authorization": f"Bearer {access_token}",
        },
    )
    # delete_img_d_data = json.loads(delete_img_d.text)
    # print("delete_img_p_data", delete_img_d_data)
```

</details>

## 2.9. Get user information:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": {
    "user_id": "a23415...",
    "user_name": "admin",
    "public_key": "118403 97093"
  }
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{ "status": "error", "code": "404", "message": "User not found" }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
    # print("public_key_g_data", user_info_g_data)
    userId = user_info_g_data["data"]["user_id"]
    userName = user_info_g_data["data"]["user_name"]
    publicKey = user_info_g_data["data"]["public_key"]
    return str(
        '{"data": {"user id": "%s", "userName": "%s", "publicKey": "%s"}}'
        % (str(userId), str(userName), str(publicKey))
    )
```

</details>

## 2.10. Get all user information:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": [
    {
      "user_id": "a23415...",
      "user_name": "admin",
      "public_key": "118403 97093"
    }
  ]
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{ "status": "success", "code": "200", "data": [] }
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
    print("public_key_g_data", user_info_g_data)
```

</details>

## 2.11. Get specific image permissions information:

Only return one permissions which match the sharedUserId.

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": { "userId": "61de598f170caaeac86ce44d", "role": "write" }
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Permission for User id not found"
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Image not found"
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
    print("permission_info_g_data", permission_info_g_data)
```

</details>

## 2.12. Get image all permissions:

Return a list of permissions for image. This response also include a CSRF token
for POST request later.

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": {
    "permissions": [{ "userId": "61de598f170caaeac86ce44d", "role": "write" }],
    "csrf_token": "eyJ0eXAi..."
  }
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": {
    "permissions": [],
    "csrf_token": "eyJ0eXAi..."
  }
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Image not found"
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
    print("permission_info_g_data", permission_info_g_data)
    cookie = permission_info_g.headers["Set-Cookie"]
    csrfKey = permission_info_g_data["csrf_token"]
```

</details>

## 2.13. Share image with specific user:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> POST </td> <td> Success </td> <td> 201 </td> <td> Created - No response </td>
</tr>
<tr>
<td> POST </td> <td> Error </td> <td> 409 </td>
<td>

```json
{
  "status": "error",
  "code": "409",
  "message": "Permission user id is already exists"
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Image not found"
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
def shareImage(fileShare, userPermission, role):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # userPermission = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    permission_info_g_data = json.loads(permission_info_g.text)
    # print("permission_info_g_data", permission_info_g_data)
    cookie = permission_info_g.headers["Set-Cookie"]
    csrfKey = permission_info_g_data["csrf_token"]

    permission_info_p = requests.post(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        data={"user_id": userPermission, "role": role},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Cookie": cookie,
            "X-CSRFToken": csrfKey,
        },
    )
    if permission_info_p.text:
        permission_info_p_data = json.loads(permission_info_p.text)
    return permission_info_p.text
    # print("permission_info_g_data", permission_info_p_data)
```

</details>

## 2.14. Edit one image permission:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> PUT </td> <td> Success </td> <td> 204 </td> <td> No Content - No response </td>
</tr>
<tr>
<td> PUT </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Permission for User id not found"
}
```

</td>
</tr>
<tr>
<td> PUT </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Image not found"
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
def editImagePermissions(fileShare, sharedUserId, role):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # sharedUserId = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    permission_info_g_data = json.loads(permission_info_g.text)
    print("permission_info_g_data", permission_info_g_data)
    cookie = permission_info_g.headers["Set-Cookie"]
    csrfKey = permission_info_g_data["csrf_token"]

    permission_info_p = requests.put(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",
        data={"role": role},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Cookie": cookie,
            "X-CSRFToken": csrfKey,
        },
    )
```

</details>

## 2.15. Delete one image permission:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> DELETE </td> <td> Success </td> <td> 204 </td> <td> No Content - No response </td>
</tr>
<tr>
<td> DELETE </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Permission for User id not found"
}
```

</td>
</tr>
<tr>
<td> DELETE </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Image not found"
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
def editImagePermissions(fileShare, sharedUserId, role):
    global access_token
    global userId

    # fileShare = "bicycle2_e.png"
    # sharedUserId = "61dd6f75cb9aa4cea4a70f0c"
    name, ext = path.splitext(fileShare)

    permission_info_g = requests.get(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    permission_info_g_data = json.loads(permission_info_g.text)
    print("permission_info_g_data", permission_info_g_data)
    cookie = permission_info_g.headers["Set-Cookie"]
    csrfKey = permission_info_g_data["csrf_token"]

    permission_info_p = requests.put(
        f"http://localhost:5000/api/v1/users/{userId}/images/{name}/permissions/{sharedUserId}",
        data={"role": role},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Cookie": cookie,
            "X-CSRFToken": csrfKey,
        },
    )
```

</details>

## 2.16. Download shared image:

Since the database didn't store private key, so client can't decrypt the image
for user

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:sharedUserId&gt/images/&ltstring:fileName&gt </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET </td> <td> Success </td> <td> 200 </td>
<td>

```json
{
  "status": "success",
  "code": "200",
  "data": {
    "img_name": "bicycle.png",
    "img_content": "\u00ff...",
    "quotient": "22 22..."
  }
}
```

</td>
</tr>
<tr>
<td> GET </td> <td> Error </td> <td> 404 </td>
<td>

```json
{
  "status": "error",
  "code": "404",
  "message": "Image not found"
}
```

</td>
</tr>
</tbody>
</table>

<details open>
<summary>Code implementation</summary>

```python
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
```

</details>

## Form validation error:

Before each POST request, typically the client has to send a GET request to get
the html form with the CSRF token. But with this server, client only get CSRF
token, then user send a POST request with the form content within the request
body. The request body then passed in the form class and validated by the form.
If the form content is failed, then the this response is sent back to client.

<table>
<tbody>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> POST </td> <td> Error </td> <td> 422 </td>
<td>

```json
{
  "status": "error",
  "message": "Username or password is invalid"
}
```

</td>
</tr>
<tr>
<td> POST </td> <td> Error </td> <td> 422 </td>
<td>

```json
{
  "status": "error",
  "message": "Password is required"
}
```

</td>
</tr>
</tbody>
</table>

## Not Authorized error:

The user ID of decoded JWT token doesn't match the resources we request.

<table>
<tbody>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET/POST/PUT/DELETE </td> <td> Error </td> <td> 401 </td>
<td>

```json
{ "status": "error", "code": "401", "message": "User is not authorized" }
```

</td>
</tr>
</tbody>
</table>

## Revoked token error:

User tries to request with the revoked token.

<table>
<tbody>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET/POST/PUT/DELETE </td> <td> Error </td> <td> 401 </td>
<td>

```json
{ "status": "error", "code": "401", "message": "Token has been revoked" }
```

</td>
</tr>
</tbody>
</table>

## Invalid token error:

User tries to request with missing token or invalid token. The message may vary.

<table>
<tbody>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET/POST/PUT/DELETE </td> <td> Error </td> <td> 422 </td>
<td>

```json
{"status":"error", "code":"422", "message":"Bad Authorization
# header. Expected 'Authorization: Bearer <JWT>'"}
```

</td>
</tr>
</tbody>
</table>

# 3. TODO:

- [ ] Set expiration time for token.
- [ ] Allow user to refresh revoked token.
- [ ] Handle expired token error.
- [ ] Add validator for only .PNG image file.
- [ ] Support more image extensions, more file types.

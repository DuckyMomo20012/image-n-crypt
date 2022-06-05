# Flask server for storing encrypted images

A safety file storage (basic)

## Tech stacks:

<p align="center">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="python" height="48" width="48" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" alt="flask" height="48" width="48" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" alt="mongodb" height="48" width="48" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" alt="docker" height="48" width="48" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jenkins/jenkins-original.svg" alt="jenkins" height="48" width="48" />
</p>

## Features:

- Registration.
- Login.
- Storing image: app client encrypt image with RSA and send request to server to store image.
  - Image encrypted is required to be **openable** and can't be recognized by attackers.
- View image list.
- Download image: client download encrypted images and decrypt it using user RSA private key.
  - Download one image.
  - Download all images.
- Share image with others: other users can download image.
- After registration, account is created with these information:
  - username.
  - ID.
  - RSA public key (provided by client app for user after registration).
- Server connect with client by using REST api.

## 1. Installation:

### 1.1. Install environment:

```console
python -m venv .venv
```

### 1.2. Activate environment:

```console
.venv\Scripts\activate
```

### 1.3. Install libs:

```console
pip install -r requirements.txt
```

### 1.4. Export PYTHONPATH (Important):

Change directory to folder `flask-server`:

Windows:

```console
set PYTHONPATH=C:/Users/Alice/Desktop/flask-server/
```

Linux:

```bash
export PYTHONPATH=$(pwd)
```

## 2. How to use:

- You can create MongoDB using sample dataset from folder `data`.
- Password and RSA private key file for sample users:

```
admin:
    password: admin
    private key: rsa_admin.txt
admin2:
    password: admin
    private key: rsa_admin2.txt
admin2:
    password: admin
    private key: rsa_admin3.txt
```

### 2.1. Rename config.py & change DB URI (Important):

- Rename `config.example.py` to `config.py`
- Change `MONGODB_HOST` to your MongoDB URI. E.g:
  `mongodb+srv://<username>:<password>@crypto-image.u1r0p.mongodb.net/CryptoImage`

### 2.1. Start server:

```console
flask run
```

### 2.2. Start client:

You can use file ["**api.py**"](./client/api.py) for custom requests:

```console
cd client & python api.py
```

or file ["**main.py**"](./client/main.py) - poorly crafted client console.

```console
cd client & python main.py
```

> **⚠️ NOTE:** If you got the error: "ModuleNotFoundError: No module named
> 'src'" or something equivalent, then you have to set the PYTHONPATH.

## 3. REST API:

> At first, the server I built was based entirely on session cookie-based
> authentication using the "Flask-Login" library. But after a few kinds of research, I switched to
> token-based authentication with "Flask-JWT-Extended" library, which uses JWT
> (JSON Web Token) to authenticate. So you may find some pieces of code that was
> use cookie I left behind.

You can use the file "api.py" to test API endpoints. For the sake of
simplicity, I stored "JWT access token", "User id" as global variables for easy
access. (You can also see that I stored cookie as a global variable too).

### 3.1. REST API endpoints:

<table>
<tbody>
<tr>
<td> Method </td>
<td> URL </td>
<td> Description </td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/auth/login </td>
<td>

[Get CSRF login token](#32-login)

</td>
</tr>
<tr>
<td> POST </td>
<td> http://localhost:5000/api/v1/auth/login </td>
<td>

[Login user](#32-login)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/auth/register </td>
<td>

[Get CSRF register token](#34-register)

</td>
</tr>
<tr>
<td> POST </td>
<td> http://localhost:5000/api/v1/auth/register </td>
<td>

[Register user](#34-register)

</td>
</tr>
<tr>
<td> POST </td>
<td> http://localhost:5000/api/v1/auth/logout </td>
<td>

[Logout user](#33-logout)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users </td>
<td>

[Get all users information](#311-get-all-user-information)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt </td>
<td>

[Get user information](#310-get-user-information)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images </td>
<td>

[Get user all images](#35-list-images)

</td>
</tr>
<tr>
<td> POST </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images </td>
<td>

[Upload image](#36-upload-image)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/download-all </td>
<td>

[Download all images](#38-download-all-images)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt </td>
<td>

[Download specific image](#37-download-image)

</td>
</tr>
<tr>
<td> DELETE </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt </td>
<td>

[Delete specific image](#39-delete-image)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions </td>
<td>

[Get all image permissions](#313-get-image-all-permissions)

</td>
</tr>
<tr>
<td> POST </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions </td>
<td>

[Share image to a specific user (Grant permission)](#314-share-image-with-specific-user)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td>
<td>

[Get specific permission of image](#312-get-specific-image-permissions-information)

</td>
</tr>
<tr>
<td> PUT </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td>
<td>

[Edit specific permission of image](#315-edit-one-image-permission)

</td>
</tr>
<tr>
<td> DELETE </td>
<td> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt/permissions/&ltstring:userPermissionId&gt </td>
<td>

[Delete specific permission of image](#316-delete-one-image-permission)

</td>
</tr>
<tr>
<td> GET </td>
<td> http://localhost:5000/api/v1/users/&ltstring:sharedUserId&gt/images/&ltstring:fileName&gt </td>
<td>

[Download shared image (the same as download specific image)](#317-download-shared-image)

</td>
</tr>
</tbody>

</table>

### 3.2. Login:

> **⚠️ NOTE:** Whenever users log in or log out, that means the user's session is over,
> so the cookie will be reset. Also, the JWT token will be sent to the blacklist.

Currently, when we log in, the JWT token is stored on the client persistently ->
Vulnerable to CSRF & XSS attacks.

> **⚠️ NOTE:** Each form has its cookie, so when we send a GET request to
> request a form to submit, we have to set a cookie for POST request

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
<summary>Example request</summary>

```python
def login(username, password):
    # global cookie
    global access_token
    global userId
    login_g = requests.get("http://localhost:5000/api/v1/auth/login")
    login_data = json.loads(login_g.text)
    if "csrf_token" not in login_data.keys():
        return login_g.text
    csrfKey = login_data["csrf_token"]
    cookie = login_g.headers["Set-Cookie"]

    # print("login_p", login_g.text)

    # NOTE: When login, cookie will be reset
    login_p = requests.post(
        "http://localhost:5000/api/v1/auth/login",
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
```

</details>

### 3.3. Logout:

> **⚠️ NOTE:** I have turned off CSRF protection for the logout route, so we
> don't have to request a CSRF key.

- After user logged out, user's JWT token will be sent to block list (revoked), so
  attacker can't use the same token to log in.
- Currently not support retrieving revoked tokens.

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

<details>
<summary>Example request</summary>

```python
def logout():
    # global cookie
    global access_token
    logout_p = requests.post(
        "http://localhost:5000/api/v1/auth/logout",
        # headers={"Cookie": cookie},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    # print("logout", logout_p.text)
    return logout_p.text
    # cookie = logout_p.headers["Set-Cookie"]
```

</details>

### 3.4. Register:

~~After registering, the user is logged in, so the cookie is reset~~. User no longer log in
after registration.

When logged in, public and private for RSA algorithm is created for user at the current directory
(the directory where the client is running):

- Public key is saved with the file name: "rsa_pub.txt".

- Private key is saved with the file name: "rsa.txt". If the file name already exists, then the file name will be appended with the timestamp. E.g: rsa_20220112162809.txt

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

<details>
<summary>Example request</summary>

```python
def register(username, password):
    # global cookie
    register_g = requests.get("http://localhost:5000/api/v1/auth/register")
    register_data = json.loads(register_g.text)
    if "csrf_token" not in register_data.keys():
        return register_g.text
    csrfKey = register_data["csrf_token"]
    cookie = register_g.headers["Set-Cookie"]

    # print("register_g", register_g.text)

    e, d, n = Crypto.generateAndWriteKeyToFile("", writeFile=True)

    register_p = requests.post(
        "http://localhost:5000/api/v1/auth/register",
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

### 3.5. List images:

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

<details>
<summary>Example request</summary>

```python
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
```

</details>

### 3.6. Upload image:

> **⚠️ NOTE:** Temporarily accepting .PNG image extension only.

When the user uploads an image (.png), the image is encrypted with a public key and
returns the encrypted image along with the "quotient.txt". The quotient later is
sent along with the image content.

- Why there is a quotient file?

When encrypting the image with RSA algorithm, the image is broken and can't open.
The main purpose of quotient is used for modulo the encrypted message, so the image **still can be
opened**, but the opener may or may not understand the image. This feature is
intentionally implemented.

- Why server only accept .png files?

Well, the client can't decrypt other file extensions than .png after encrypted, so
it's a one-way upload if you use other extensions. However, if you want, you can tweak accept file extensions in file [app.py](./app.py)

- Where the images are saved?

In MongoDB cluster and [local (./src/assets/)](./src/assets/). You can also
change local save location in file [app.py](./app.py)

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images </td>
</tr>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
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

<details>
<summary>Example request</summary>

```python
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
    # fileName_encrypt = name + "_e" + ext
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
        # print("upload_img_p", upload_img_p.text)
        return upload_img_p.text
```

</details>

### 3.7. Download image:

The URI should not have the file extension.

The file is downloaded then the client uses the private key from local and the
quotient content downloaded to decrypt the message.

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

<details>
<summary>Example request</summary>

```python
def downloadImage(downloadFile, privateKeyPath):
    # global cookie
    global access_token
    global userId
    # downloadFile = "bicycle2_e.png"
    name, ext = path.splitext(downloadFile)
    # downloadFile_d = name + "_d" + ext
    downloadFile_d = name + ext
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
    Crypto.decrypt(
        imgEncryptedPath=downloadFile,
        privateKeyPath=privateKeyPath,
        imgDecryptedSaveDst=downloadFile_d,
    )
```

</details>

### 3.8. Download ALL images:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/download-all </td>
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

<details>
<summary>Example request</summary>

```python
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
        Crypto.decrypt(
            imgEncryptedPath=imgName,
            privateKeyPath=pathPrivateKey,
            imgDecryptedSaveDst=imgName,
        )
```

</details>

### 3.9. Delete image:

<table>
<tbody>
<tr>
<td> URL </td> <td colspan=3> http://localhost:5000/api/v1/users/&ltstring:userId&gt/images/&ltstring:fileName&gt </td>
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
{ "status": "error", "code": "404", "message": "Image not found" }
```

</td>
</tr>
</tbody>
</table>

<details>
<summary>Example request</summary>

```python
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
```

</details>

### 3.10. Get user information:

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

<details>
<summary>Example request</summary>

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
```

</details>

### 3.11. Get all user information:

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

<details>
<summary>Example request</summary>

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
    # print("public_key_g_data", user_info_g_data)
    return user_info_g.text
```

</details>

### 3.12. Get specific image permissions information:

Only return one permission that matches the sharedUserId.

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

<details>
<summary>Example request</summary>

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
    # print("permission_info_g_data", permission_info_g_data)
    return permission_info_g.text
```

</details>

### 3.13. Get image all permissions:

Return a list of permissions for the image. This response also includes a CSRF token
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

<details>
<summary>Example request</summary>

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
    if permission_info_g_data["status"] == "error":
        return permission_info_g.text
    # print("permission_info_g_data", permission_info_g_data)
    # cookie = permission_info_g.headers["Set-Cookie"]
    # csrfKey = permission_info_g_data["csrf_token"]
    return str(
        '{"data": {"permissions": "%s"}}'
        % (str(permission_info_g_data["data"]["permissions"]))
    )
```

</details>

### 3.14. Share image with a specific user:

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

<details>
<summary>Example request</summary>

```python
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
```

</details>

### 3.15. Edit one image permission:

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

<details>
<summary>Example request</summary>

```python
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
```

</details>

### 3.16. Delete one image permission:

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

<details>
<summary>Example request</summary>

```python
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
```

</details>

### 3.17. Download shared image:

Since the database didn't store a private key, so the client can't decrypt the image
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

<details>
<summary>Example request</summary>

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
```

</details>

### 3.18. Form validation error:

Before each POST request, typically the client has to send a GET request to get
the html form with the CSRF token. But with this server, the client only gets CSRF
token, then the user sends a POST request with the form content within the request
body. The request body then passed in the form class and was validated by the form.
If the form content is failed, then this response is sent back to the client.

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

### 3.19. Not Authorized error:

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

### 3.20. Revoked token error:

The user tries to request with the revoked token.

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

### 3.21. Invalid token error:

The user tries to request with the missing token or invalid token. The message may vary.

<table>
<tbody>
<tr>
<td> Method </td> <td> Status </td> <td> Code </td> <td> Response </td>
</tr>
<tr>
<td> GET/POST/PUT/DELETE </td> <td> Error </td> <td> 422 </td>
<td>

```json
{
  "status": "error",
  "code": "422",
  "message": "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"
}
```

</td>
</tr>
</tbody>
</table>

## 4. RSA encryption algorithm:

### 4.1. Generate keys:

Code for Extended Euclid can be found in file [crypto.py](https://github.com/DuckyMomo20012/crypto/blob/master/src/helpers/crypto/crypto.py#L15)

<details>
<summary>Code implementation</summary>

```python
def generateKeys(p, q):
    n = calculate_n(p, q)
    phi_n = calculate_phi_n(q, p)
    u, x, d = 0, 0, 0
    e = 0
    while u != 1:
        e = random.randint(2, phi_n - 1)
        u, x, d = GCD(phi_n, e)
        if d < 0:
            d = phi_n + d
    return n, e, d
```

</details>

### 4.2. Encryption:

<details>
<summary>Code implementation</summary>

```python
def encrypt(
    imgPath,
    e=None,
    n=None,
    publicKeyPath=None,
    imgEncryptedSaveDst="encode_img.png",
    quotientSaveDst="quotient.txt",
):
    if not publicKeyPath and not e and not n:
        raise Exception("Public key is missing")
    # e, n directly passed into function has more priority than text file
    if publicKeyPath and not e and not n:
        publicKey = readFile(publicKeyPath)
        n, e = map(int, publicKey.split(" "))

    if not e or not n and not publicKeyPath:
        raise Exception("Public key is missing.")

    if not os.path.exists(imgPath):
        raise Exception("Image path is not exist")

    img = cv2.imread(imgPath)

    f = open(quotientSaveDst, "w")
    for i in range(3):
        for j in range(img.shape[0]):
            for l in range(img.shape[1]):
                pixel = img[j, l, i]
                remainder1 = powermod(pixel, e, n)
                remainder2 = powermod(remainder1, 1, 256)
                quotient = int(remainder1 / 256)
                img[j, l, i] = remainder2
                f.write(str(quotient) + " ")
    f.close()
    cv2.imwrite(imgEncryptedSaveDst, img)
    return img
```

</details>

### 4.3. Decryption:

<details>
<summary>Code implementation</summary>

```python
def decrypt(
    imgEncryptedPath,
    d=None,
    n=None,
    privateKeyPath=None,
    imgDecryptedSaveDst="decode_img.png",
    quotientPath="quotient.txt",
):
    if not privateKeyPath and not d and not n:
        raise Exception("Private key is missing")
    # d, n directly passed into function has more priority than text file
    if privateKeyPath and not d and not n:
        private_key = readFile(privateKeyPath)
        d, n = map(int, private_key.split(" "))

    if not os.path.exists(imgEncryptedPath):
        raise Exception("Image path is not exist")

    if not os.path.exists(quotientPath):
        raise Exception("Quotient path is not exist")

    img = cv2.imread(imgEncryptedPath)
    quotient = readFile(quotientPath)
    list_quotient = quotient.split(" ")

    index = 0
    for i in range(3):
        for j in range(img.shape[0]):
            for l in range(img.shape[1]):
                pixel = img[j, l, i]
                c = pixel + int(list_quotient[index]) * 256
                img[j, l, i] = powermod(c, d, n)
                index = index + 1
    cv2.imwrite(imgDecryptedSaveDst, img)
    return img
```

</details>

## 5. TODO:

- [x] Important: Remove entirely CSRF protection. Keeps CSRF for Authentication
- [x] Set the expiration time for the token (NOTE: Added but don't know if it works)
- [x] Add validator for only .PNG image file.
- [ ] Allow user to get back revoked token.
- [ ] Handle expired token error.
- [ ] Support more image extensions, more file types.
- [ ] Client support decrypt image service.
- [ ] Handle file permissions (read/write)

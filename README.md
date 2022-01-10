<style>
    table {
        width: 100%;
    }
</style>
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

## 2.1. Login:

> NOTE: Whenever User login or logout, that means user's session is over, so cookie will be reset.

> After register, user is logged in, so cookie is reset.

```python
login_g = requests.get("http://localhost:5000/api/login")
login_data = json.loads(login_g.text)
csrfKey = login_data["csrf_token"]
cookie = login_g.headers["Set-Cookie"]
print("login_p", login_g.text)
# NOTE: When login, cookie will be reset
login_p = requests.post(
    "http://localhost:5000/api/login",
    data={"username": "admin", "password": "admin", "csrf_token": csrfKey},
    headers={
        "X-CSRFToken": csrfKey,
        "Cookie": cookie,
    },
)
print("login_p", login_p.text)
cookie = login_p.headers["Set-cookie"]
```

<table>
<td> URL </td>
<td> http://localhost:5000/api/login </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "csrf_token": "IjA5Z...",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Success </td>
<td>

```json
{
  "data": {
    "public_key": "34609 28407",
    "username": "vinh"
  },
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
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
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "Password is required"
}
```

</td>
</tr>
</table>

## 2.2. Logout:

> NOTE: When logout, cookie will be reset

> NOTE: I have turned off csrf protection for logout route, so we don't have to request a CSRF key.

> NOTE: Unauthorized request will return "User is not authorized"

```python
logout_p = requests.post(
    "http://localhost:5000/api/logout",
    headers={"Cookie": cookie},
)
print("logout", logout_p.text)
cookie = logout_p.headers["Set-Cookie"]
```

<table>
<td> URL </td>
<td> http://localhost:5000/api/logout </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> POST </td>
<td> Success </td>
<td>

```json
{
  "data": "User logged out",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "User is not authorized"
}
```

</td>
</tr>
</table>

## 2.3. Register:

```python
register_g = requests.get("http://localhost:5000/api/register")
register_data = json.loads(register_g.text)
csrfKey = register_data["csrf_token"]
cookie = register_g.headers["Set-Cookie"]
print("register_g", register_g.text)
e, d, n = function_support.create_write_key("", writeFile=True)
register_p = requests.post(
    "http://localhost:5000/api/register",
    data={"username": "admin", "password": "admin", "publicKey": f"{n} {e}"},
    headers={
        "X-CSRFToken": csrfKey,
        "Cookie": cookie,
    },
)
print("register_p", register_p.text)
```

<table>
<td> URL </td>
<td> http://localhost:5000/api/register </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "csrf_token": "IjA5Z...",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Success </td>
<td>

```json
{
  "data": {
    "public_key": "34609 28407",
    "username": "vinh"
  },
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "Username already exists"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "Password is required, Public key is required"
}
```

</td>
</tr>
</table>

## 2.4. List images:

```python
list_img_g = requests.get(
    "http://localhost:5000/api/image-list", headers={"Cookie": cookie}
)
print("list_img_g", list_img_g.text)
```

<table>
<td> URL </td>
<td> http://localhost:5000/api/image-list </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "status": "success",
  "data": ["traffic-sign.png", "bicycle.png"]
}
```

</td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "status": "success",
  "message": "No image on database"
}
```

</td>
</tr>
</table>

## 2.5. Upload image:

> NOTE: Temporarily accepting .PNG image extension only.

```python
public_key_g = requests.get(
    "http://localhost:5000/api/public-key", headers={"Cookie": cookie}
)
public_key_data = json.loads(public_key_g.text)
print("public_key_data", public_key_data)
n, e = map(int, public_key_data["public_key"].split(" "))
upload_img_g = requests.get(
    "http://localhost:5000/api/upload-image", headers={"Cookie": cookie}
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
        "http://localhost:5000/api/upload-image",
        files={"imageFile": f},
        data={"quotient": quotient},
        headers={
            "X-CSRFToken": csrfKey,
            "Cookie": cookie,
        },
    )
    print("upload_img_p", upload_img_p.text)
```

<table>
<td> URL </td>
<td> http://localhost:5000/api/upload-image </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "csrf_token": "IjA5Z...",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Success </td>
<td>

```json
{
  "data": {
    "img_name": "bicycle.png_20220109213826"
  },
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "Image file is required"
}
```

</td>
</tr>
</table>

## 2.6. Download image:

```python
downloadFile = "bicycle2_e.png"
downloadFile_d = "bicycle_d.png"
download_img_g = requests.get(
    f"http://127.0.0.1:5000/api/download/{downloadFile}",
    headers={"Cookie": cookie},
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
```

<table>
<td> URL </td>
<td> http://127.0.0.1:5000/api/download/{downloadFile} </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "status": "success",
  "data": {
    "img_content": "\u00ff...",
    "img_name": "bicycle.png"
  }
}
```

</td>
</tr>
<tr>
<td> GET </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "Image not found"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "User not found"
}
```

</td>
</tr>
</table>

## 2.7 Download ALL images:

```python
download_img_all_g = requests.get(
    f"http://127.0.0.1:5000/api/download-all",
    headers={"Cookie": cookie},
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
```

<table>
<td> URL </td>
<td> http://127.0.0.1:5000/api/download-all </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "status": "success",
  "data": [
    {
      "img_content": "\u00ff...",
      "img_name": "bicycle.png"
    }
  ]
}
```

</td>
</tr>
<tr>
<td> GET </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "Image not found"
}
```

</td>
</tr>
<tr>
<td> GET </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "User not found"
}
```

</td>
</tr>
</table>

## 2.8. Delete image:

```python
deleteFile = "bicycle2_e.png"
delete_img_g = requests.get(
    f"http://127.0.0.1:5000/api/delete/{deleteFile}", headers={"Cookie": cookie}
)
delete_img_g_data = json.loads(delete_img_g.text)
print("delete_img_g_data", delete_img_g_data)
csrfKey = delete_img_g_data["csrf_token"]
delete_img_p = requests.post(
    f"http://127.0.0.1:5000/api/delete/{deleteFile}",
    headers={
        "X-CSRFToken": csrfKey,
        "Cookie": cookie,
    },
)
delete_img_p_data = json.loads(delete_img_p.text)
print("delete_img_p_data", delete_img_p_data)
```

<table>
<td> URL </td>
<td> http://127.0.0.1:5000/api/delete/{deleteFile} </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "csrf_token": "IjA5Z...",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Success </td>
<td>

```json
{
  "data": "Image deleted",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> POST </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "User not found"
}
```

</td>
</tr>
</table>

## 2.9. Get public key:

```python
public_key_g = requests.get(
    "http://127.0.0.1:5000/api/public-key",
    headers={
        "Cookie": cookie,
    },
)
public_key_g_data = json.loads(public_key_g.text)
print("public_key_g_data", public_key_g_data)
```

<table>
<td> URL </td>
<td> http://127.0.0.1:5000/api/public-key </td>
</table>
<table>
<tr>
<td> Method </td> <td> Status </td> <td> Response </td>
</tr>
<tr>
<td> GET </td>
<td> Success </td>
<td>

```json
{
  "public_key": "118403 97093",
  "status": "success"
}
```

</td>
</tr>
<tr>
<td> GET </td>
<td> Error </td>
<td>

```json
{
  "status": "error",
  "message": "User not found"
}
```

</td>
</tr>
</table>

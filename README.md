# 1. Installation:
## 1.1. Install environment:
```console
python -m venv .venv
```
# 1.2. Activate enviroment:
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
> NOTE: Only **Login** GET request have "Set-Cookie" header
```python
login_g = requests.get("http://localhost:5000/api/login")
login_data = json.loads(login_g.text)
csrfKey = login_data["csrf_token"]
cookie = login_g.headers["Set-Cookie"]
print("login_p", login_g.text)
# NOTE: Every POST request, cookie will be reset
login_p = requests.post(
    "http://localhost:5000/api/login",
	data={
		"username": "admin",
		"password": "admin",
		"csrf_token": csrfKey
	},
	headers={
		"X-CSRFToken": csrfKey,
		"Cookie": cookie,
	},
)
print("login_p", login_p.text)
cookie = login_p.headers["Set-cookie"]
```

> Success: { "data":{"public_key":null,"username":"admin"},"status":"success"}

> Error: {"message":"Username or password is invalid","status":"error"}

## 2.2. Logout:
> NOTE: Every POST request, cookie will be reset.

> NOTE: I have turned off csrf protection for logout route, so we don't have to request a CSRF key.
```python
logout_p = requests.post(
	"http://localhost:5000/api/logout",
	headers={
		"Cookie": cookie
	},
)
print("logout", logout_p.text)
```

> Success: {"data":"User logged out","status":"success"}

> NOTE: Unauthorized request will return this error

> Error: {"message":"User is not authorized","status":"error"}

## 2.3. Register:
```python
register_g = requests.get("http://localhost:5000/api/register")
register_data = json.loads(register_g.text)
csrfKey = register_data["csrf_token"]
cookie = register_g.headers["Set-Cookie"]
print("register_g", register_g.text)

register_p = requests.post(
	"http://localhost:5000/api/register",
	data={
		"username": "admin",
		"password": "admin",
		"publicKey": "34609 28407"
	},
	headers={
		"X-CSRFToken": csrfKey,
		"Cookie": cookie,
	},
)
print("register_p", register_p.text)
```

> Success: {"data":{"public_key":"34609 28407","username":"vinh"},"status":"success"}

> Error: {"message":"Username already exists","status":"error"}

## 2.4. List images:
```python
list_img_g = requests.get(
	"http://localhost:5000/api/image-list",
	headers={
		"Cookie": cookie
	}
)
print("list_img_g", list_img_g.text)
```

>  Success: {"data":["traffic-sign.png","bicycle.png"],"status":"success"}

>  Success: {"status": "success", "data": "No image"}

## 2.5. Download image:
```python
downloadFile = 'bicycle.jpg'
download_img_g = requests.get(
	f"http://127.0.0.1:5000/api/image-list/download/{downloadFile}",
	headers={
		"Cookie": cookie
	},
)

data = json.loads(download_img_g.text)
imgData = data["data"]["img_content"]
imgName = data["data"]["img_name"]
with open(imgName, "wb") as f:
	f.write(imgData.encode("ISO-8859-1"))
```

> Success: {"data":{"img_content":"\u00ff...","img_name":"bicycle.png"},"status":"success"}

> Error: {"message":"Image not found","status":"error"}

## 2.6. Upload image:
```python
upload_img_g = requests.get(
	"http://localhost:5000/api/upload-image",
	headers={
		"Cookie": cookie
	}
)
upload_img_data = json.loads(upload_img_g.text)
csrfKey = upload_img_data["csrf_token"]
print("upload_img_g", upload_img_g.text)

# NOTE: "imageFile" is field from ImageForm class

fileName = 'bicycle.jpg'
with open(fileName, 'rb') as f:
	upload_img_p = requests.post(
		"http://localhost:5000/api/upload-image",
		files={
			"imageFile": f
		},
		headers={
			"X-CSRFToken": csrfKey,
			"Cookie": cookie,
		},
 	)
 print("upload_img_p", upload_img_p.text)
```

> Success: {"data":{"img_name":"bicycle.png_20220109213826"},"status":"success"}
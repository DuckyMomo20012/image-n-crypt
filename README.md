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
set PYTHONPATH=%cd%
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

This section has moved to [Wiki](https://github.com/DuckyMomo20012/flask-server/wiki), [REST API endpoints](https://github.com/DuckyMomo20012/flask-server/wiki/REST-API-endpoints) page.

## 4. RSA encryption algorithm:

This section has moved to
[Wiki](https://github.com/DuckyMomo20012/flask-server/wiki), [RSA encryption algorithm](https://github.com/DuckyMomo20012/flask-server/wiki/RSA-encryption-algorithm) page.

## 5. TODO:

- [x] Important: Remove entirely CSRF protection. Keeps CSRF for Authentication
- [x] Set the expiration time for the token (NOTE: Added but don't know if it works)
- [x] Add validator for only .PNG image file.
- [ ] Allow user to get back revoked token.
- [ ] Handle expired token error.
- [ ] Support more image extensions, more file types.
- [ ] Client support decrypt image service.
- [ ] Handle file permissions (read/write)

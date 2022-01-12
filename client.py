import requests
from bs4 import BeautifulSoup
import json
from requests.sessions import session
import pickle

url = "http://localhost:5000/api/login"

# save cookie
def save_cookies(requests_cookiejar, filename):
    with open(filename, "wb") as f:
        pickle.dump(requests_cookiejar, f)


# load cookie
def load_cookies(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def client(username, password, filename):

    # save cookies
    r = requests.get(url)
    save_cookies(r.cookies, filename)

    # load cookies and do a request
    client_ = requests.get(url, cookies=load_cookies(filename))

    print(client_.status_code)

    if client_.status_code == 200:
        print("Success!")
    elif client_.status_code == 404:
        print("Not Found.")

    payload = {"username": username, "password": password}
    with session() as s:
        r = requests.post(url, data=payload)
        print(r)
        print(r.content)

    r = requests.session()

    data = {"username": "admin", "password": "admin"}
    r = requests.post(url, data=payload)
    cookie = client_.headers["Set-Cookie"]
    print(client_.text)


# if __name__ == "__main__":
#     ans = True
#     while ans:
#         print("  1. Login ")
#         print("  2.Register")

#         ans = input("What would you like to do?")
#         if ans == "1":
#             ans = True
#             while ans:
#                 login()  # gọi hàm login
#                 print("  1. List image ")
#                 print("  2. Upload image")

#         elif ans == "2":
#             print("\n ...")

#     client()

import requests
from bs4 import BeautifulSoup
import json

from requests.sessions import session 
url = "http://localhost:5000/api/login"
#url = "https://zingmp3.vn/"
data = {'username':'codernothacker', 'password': 'nopass'}
res = requests.post(url, json = data)

if res.status_code == 200:
    print ('Success!')
elif res.status_code == 404:
    print('Not Found.')

print(res.json)

def login( username, password):
    s = requests.Session()
    payload = {
        'username':username, 
        'password': password
        }
    res = s.post('http://localhost:5000/api/login', json = payload)
    s.headers.update({'login': json.loads(res.content)['token']})
    print(res.content)
    return s

session = login('codernothacker','nopass')
r = session.patch('http://localhost:5000/api/login')
print(r.content)
import requests
from bs4 import BeautifulSoup

# r = requests.get('http://localhost:5000/api/register')
# print("r", r.text)
# token_el = BeautifulSoup(r.json()['csrf_token'], 'html.parser')
# token_val = token_el.input.attrs['value']
# print("token_val", type(token_val))

# custom_header = {
# 	"X-CSRFToken": token_val
# }
p = requests.post('http://localhost:5000/api/login', data=dict({
	"username": 'duckymomo',
	"password": 'asdfasdf'
}))
print(p.text)

logout = requests.get('http://localhost:5000/api/logout')
print("logout", logout.text)

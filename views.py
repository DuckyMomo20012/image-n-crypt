from flask import request, session
from app import app
from model import User, LoginForm



@app.route("/", methods = ['GET', 'POST'])
def index():
	user = User(username = 'Vinh')
	user.save()
	return user.username;

# @csrf.exempt
@app.route("/api/register", methods = ['GET', 'POST'])
def login():
	# pass request data to form
	form = LoginForm()
	if request.method == 'POST':
		# Don't have to pass request.form or check POST request, because
		# validate_on_submit automatically do that
		if form.validate_on_submit():
			print('Valid')
			return 'Valid'
		else:
			print(form.errors)

	return 'result'

# with app.test_client() as c:
# 	rv = c.get('/api/register', data=dict(
# 		username='vinh',
# 		password='asdfasdf',
# 	))
# 	csrf_token = str(rv.data)
# 	rv = c.get('/api/register', data=dict(
# 		username='vinh',
# 		password='asdfasdf',
# 	))
# 	print(rv.data)
	# json_data = rv.get_json()

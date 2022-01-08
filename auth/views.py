from flask import request, render_template, url_for, flash, session
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from app import app, login_manager
from auth.model import User, LoginForm
from auth.service import getUserById, getUserByUserName
from flask_login import login_user, login_required, AnonymousUserMixin
import bcrypt
import json

@login_manager.user_loader
def load_user(user_id):
    userDoc = getUserById(user_id)
    if (not userDoc):
        return AnonymousUserMixin()

    userObj = json.loads(userDoc.to_json())
    # id field inherited from UserMixin class (from flask_login)
    user = User(id=userObj['_id']['$oid'], username=userObj['username'], password=userObj['password'])
    return user

@login_manager.unauthorized_handler
def unauthorized():
    # Flash all flash messages before
    session.pop('_flashes', None)
    flash('Please login to continue')
    # If unauthorize then redirect to login
    return redirect(url_for('login'))

# @csrf.exempt
@app.route("/api/register", methods = ['GET', 'POST'])
def register():
    # pass request data to form
    form = LoginForm()
    if request.method == 'POST':
        # Don't have to pass request.form or check POST request, because
        # validate_on_submit automatically do that

        if form.validate_on_submit():
            data = request.form
            username = data['username']
            password = data['password'].encode()

            users = getUserByUserName(username)

            if len(users) > 0:
                flash('Username already exists');
                return redirect(url_for('register'))

            salt = bcrypt.gensalt(rounds=16)

            hashPassword = bcrypt.hashpw(password, salt)
            user = User(username=username, password=hashPassword)
            user.save()

            login_user(user)

            flash('Account register successfully')
            return redirect(url_for('index'))
        else:
            flash(form.errors)
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route("/api/login", methods = ['GET', 'POST'])
def login():
    # pass request data to form
    form = LoginForm()

    # Don't have to pass request.form or check POST request, because
    # validate_on_submit automatically do that
    if form.validate_on_submit():
        data = request.form
        username = data['username']
        password = data['password'].encode()
        user = getUserByUserName(username).first()
        if (not user):
            return redirect(url_for('login'))
        # print(user.to_json())
        if bcrypt.checkpw(password, user.password.encode()):
            login_user(user)
            flash('Logged in')
            return redirect(url_for('index'))
        else:
            return 'Invalid information'

    return render_template('login.html', form=form)

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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

from flask import redirect, request, url_for, render_template
from flask_login import current_user, login_user, logout_user
from Models.usermodel import User
from Utilities.Db_utilities import get_db, get_user_id
from .backend import create_user, name_available, password_acceptor, check_password, hash
from . import login


@login.route('/', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('login.html')

@login.route('/', methods=['POST'])
def login_form():
    username = request.form.get('user_name')
    password = request.form.get('password')
    user_id = get_user_id(username)
    if (user_id): 
        user = User(user_id)
    else:
        user = None
    if user and check_password(user, password):
        login_user(user)
    else: 
        print('failed to log in')
        print(password)
    return redirect(url_for('Login.login_page'))

@login.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('Login.login_page'))

@login.route('/create_user', methods=['GET'])
def create_user_page():
    return render_template('create_user.html')

@login.route('/create_user', methods=['POST'])
def create_user_form():
    conn=get_db()
    user_name = request.form['user_name']
    password=request.form['password']
    if (not name_available(user_name)):
        return render_template('fail.html', reason="user name taken")
    if (not password_acceptor(password)):
        return render_template('fail.html', reason="password not accepted")
    create_user(user_name, hash(password))
    return redirect(url_for('Login.login_page'))
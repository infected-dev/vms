from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user
from flaskapp.models import User
from flaskapp import login_manager
from flaskapp.dataentry import post_format


#Register the File as Blueprint
auth = Blueprint('auth', __name__)


#Loggin in Route
@auth.route('/login', methods=['POST'])
def login_main():
    user_get = request.form.get('username')
    user_pwd_get = request.form.get('password')
    user = User.query.filter_by(id=user_get).first()
    #Checking username password 
    if user.password == user_pwd_get:
        login_user(user, remember=True)
        flash('Successfully logged in')
        return redirect(url_for('dataentry.post_format'))
    else: 
        flash('wrong password or Username')
        return redirect(url_for('base.index'))


#Logging Out Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User Logged out')
    return redirect(url_for('base.index'))
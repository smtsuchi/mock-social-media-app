from . import bp as auth
from app import db
from flask import render_template, request, flash, redirect, url_for, jsonify
from .forms import UserInfoForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

@auth.route('/register', methods=['GET','POST'])
def register():
    data = request.json
    # form = UserInfoForm()
    # print(form)
    
    if request.method == 'POST' and data['password'] == data['confirm_password']:
        # password = form.password.data
        token = None
        token_exp = None
        u = User(data['username'],data['email'],data['password'])
        print(u.to_dict())
        db.session.add(u)
        db.session.commit()
        return jsonify(u.to_dict())

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.json
        username = data['username']
        password = data ['password']
        # print(data['username'])
        user = User.query.filter_by(username=username).first()
        # print(user)
        if user is None or not check_password_hash(user.password, password):
            return None
        login_user(user, remember = True)
        print(current_user)
        return jsonify(user.to_dict())
    print(current_user.is_authenticated)
    return jsonify({
        "authenticated": current_user.is_anonymous
    })

    
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return "user logged out"

# @auth.route('/myinfo')
# @login_required
# def myInfo():

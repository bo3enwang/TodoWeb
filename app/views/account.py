# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from ._base import lm
from app.models import db, User
from app.forms import LoginForm, RegisterForm

account = Module(__name__)


@lm.user_loader
def load_user(userid):
    return User.query.get(userid)


@account.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@account.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.login.data, form.password.data)
        if user and authenticated:
            remember = form.remember.data
            login_user(user, remember)
            return redirect(url_for('todo.index'))
        else:
            flash("对不起, 用户名或密码错误", "error")
    return render_template('account/login.html', form=form)


@account.route('/index')
@login_required
def index():
    return render_template('account/index.html')


# 注册
# @account.route('/register', methods=("GET", "POST"))
# def register():
#     form = RegisterForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         u = User()
#         u.username = form.username.data
#         u.password = form.password.data
#         u.email = form.email.data
#         db.session.add(u)
#         db.session.commit()
#         flash("注册成功,请登录", "error")
#         return redirect(url_for('login', type='register'))
#     return render_template('account/register.html', form=form)


# 用户名重复验证
@account.route('/validate/username', methods=("POST",))
def validate_username():
    valid = True
    username = request.form['username']
    if username and User.query.filter(User.username == username).count() > 0:
        valid = False
    return jsonify({'valid': valid})


# 邮箱重复验证
@account.route('/validate/email', methods=("POST",))
def validate_email():
    valid = True
    email = request.form['email']
    if email and User.query.filter(User.email == email).count() > 0:
        valid = False
    return jsonify({'valid': valid})

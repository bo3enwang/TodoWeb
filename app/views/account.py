# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from ._base import lm
from app.models import User
from app.forms import LoginForm

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
    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.login.data, form.password.data)
        if user and authenticated:
            remember = form.remember.data
            login_user(user, remember)
            return redirect(url_for('project.project_query',ptype='progress'))
    else:
        flash("对不起, 用户名或密码错误", "error")
    return render_template('account/login.html', form=form)


@account.route('/index')
@login_required
def index():
    return render_template('account/index.html')

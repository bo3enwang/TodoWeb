# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from app import lm
from app.models.users import User
from flask import Module,render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from datetime import datetime
from app import db


account = Module(__name__)

# flask-login
@lm.user_loader
def load_user(userid):
    return User.query.get(userid)


@account.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@account.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@account.route('/')
@account.route('/index')
def index():
    form = LoginForm()
    if g.user.is_authenticated():
        return redirect(request.args.get('next') or url_for('myproject'))
    return render_template('index.html', form=form)


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_info = form.validate_login()
        if login_info['result'] == 0:
            flash(login_info['msg'])
            return redirect(url_for('index'))
        remember_me = form.remember_me.data
        user = form.get_user()
        login_user(user, remember_me)
        return redirect(request.args.get('next') or url_for('myproject'))
    else:
        return render_template('index.html', form=form)
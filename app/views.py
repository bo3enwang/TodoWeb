# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from app import app, lm
from models import User
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm,AddTaskForm
from datetime import datetime
from app import db


# flask-login
@lm.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    if g.user.is_authenticated():
        return redirect(request.args.get('next') or url_for('mytask'))
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
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
        return redirect(request.args.get('next') or url_for('mytask'))
    else:
        return render_template('index.html', form=form)


@app.route('/addtask')
def addTask():
    return ''


@app.route('/task')
@login_required
def mytask():
    form = AddTaskForm()
    return render_template('task.html',form = form)


@app.route('/todo')
@login_required
def mytodo():
    return render_template('todo.html')

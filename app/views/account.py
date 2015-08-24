# -*- coding:utf8 -*- 
__author__ = 'Zovven'

# from app import lm
# from app.models.users import User
from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
# from flask.ext.login import login_user, logout_user, current_user, login_required
# from app.forms import LoginForm
# from datetime import datetime
# from app import db


account = Module(__name__)


@account.route("/login/", methods=("GET", "POST"))
def login():
    return render_template('account/index.html')

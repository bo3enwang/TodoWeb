# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from ._base import lm

todo = Module(__name__)


@todo.route('/p')
def index():
    return render_template('todo/todo.html')

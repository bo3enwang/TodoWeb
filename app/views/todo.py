# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from app.models import Todo

todo = Module(__name__)


@todo.route('/p/data', methods=("post",))
def project_data():
    jsondata = request.get_json()
    t_date = jsondata.get('t_date')
    tododata = Todo.query.query_day(t_date).restricted(g.user).jsonify()
    return jsonify({"result": tododata})


@todo.route('/p')
def index():
    return render_template('todo/todo.html')

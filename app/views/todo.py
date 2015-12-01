# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from app.models import Todo, db
from app.forms import TodoAddForm

todo = Module(__name__)


@todo.route('')
def todo_list():
    return render_template("admin/todoList.html")


# @todo.route('/add', methods=("post",))
# @login_required
# def todo_add():
#     form = TodoAddForm()
#     result = -1
#     if form.validate_on_submit():
#         t = Todo()
#         t.name = form.name.data
#         t.t_date = form.t_date.data
#         t.user = g.user
#         db.session.add(t)
#         db.session.commit()
#         result = 1
#     return jsonify({'result': result})
#
#
# @todo.route('/p')
# @login_required
# def index():
#     form = TodoAddForm()
#     return render_template('todo/todo.html', form=form)
#
#
# @todo.route('/change', methods=("post",))
# @login_required
# def change_todo_status():
#     result = -1
#     jsondata = request.get_json()
#     todoid = jsondata.get('id')
#     status = jsondata.get('status')
#     t = Todo.query.get(todoid)
#     if t:
#         if status == 1:
#             t.status = 1
#         else:
#             t.status = 0
#         db.session.commit()
#         result = 1
#     return jsonify({'result': result})
#
#
# @todo.route('/delete', methods=("post",))
# @login_required
# def delete_todo():
#     result = -1
#     jsondata = request.get_json()
#     todoid = jsondata.get('id')
#     t = Todo.query.get(todoid)
#     if t:
#         db.session.delete(t)
#         db.session.commit()
#         result = 1
#     return jsonify({'result': result})

# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from app.models import Todo, db
from app.forms import TodoAddForm, TodoCompeteForm

todo = Module(__name__)


@todo.route('/json', methods=("post",))
def todo_json():
    post_data = request.get_json()
    start_date = post_data.get('start_date')
    end_date = post_data.get('end_date')
    json_data = Todo.query.search_date(start_date, end_date).sort_by_type()
    return jsonify(success=True, result=list(json_data.jsonify()))


@todo.route('')
def todo_list():
    add_form = TodoAddForm()
    complete_form = TodoCompeteForm()
    return render_template("admin/todoList.html", add_form=add_form, complete_form=complete_form)


@todo.route('/add', methods=("post",))
def todo_add():
    add_form = TodoAddForm()
    if add_form.validate_on_submit():
        _todo = Todo()
        add_form.populate_obj(_todo)
        db.session.add(_todo)
        db.session.commit()
        flash("新增待办成功", "success")
        return redirect(url_for("todo_list"))
    flash("新增待办失败", "success")
    return redirect(url_for("todo_list"))


@todo.route('/complete', methods=("post",))
def todo_complete():
    complete_form = TodoCompeteForm()
    if complete_form.validate_on_submit():
        _todo = Todo.query.get_or_404(complete_form.todo_id.data)
        _todo.todo_status = Todo.STATUS_DONE
        complete_form.populate_obj(_todo)
        db.session.commit()
        return jsonify(success=True, todo=_todo.json)
    return jsonify(success=False)


@todo.route('/api/add', methods=("post",))
def todo_add_from_plan():
    json_data = request.get_json()
    todo_desc = json_data.get('todo_desc')
    if todo_desc is not None:
        _todo = Todo()
        _todo.todo_desc = todo_desc
        _todo.todo_type = Todo.TYPE_PLAN
        db.session.add(_todo)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@todo.route("/<int:todo_id>/delete/", methods=("post",))
def todo_delete(todo_id):
    _todo = Todo.query.get_or_404(todo_id)
    db.session.delete(_todo)
    db.session.commit()
    return jsonify(success=True)

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

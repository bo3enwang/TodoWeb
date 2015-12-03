# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import func, and_
from app.models import Todo, db
from app.forms import TodoAddForm, TodoCompeteForm
import json
from app.jsonutil import DecimalEncoder

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


@todo.route('/chart/pie', methods=("post",))
def todo_chart_json():
    post_data = request.get_json()
    start_date = post_data.get('start_date')
    end_date = post_data.get('end_date')
    rs = db.session.query(Todo.todo_type, func.sum(Todo.todo_time)).filter(
        and_(Todo.todo_date >= start_date, Todo.todo_date <= end_date)).all()
    type_dict = {
        "0": "计划",
        "1": "紧急",
        "2": "优先",
        "3": "普通",
    }
    json_list = list()
    for row in rs:
        json_dict = dict()
        json_dict['name'] = type_dict[str(row[0])]
        json_dict['value'] = long(row[1])
        json_list.append(json_dict)
    return jsonify(success=True, result=json_list)

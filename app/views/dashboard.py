# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from app.models import Todo, db
from app import timeutils
from flask.ext.login import login_required

dashboard = Module(__name__)


@dashboard.route("")
@dashboard.route("/dashboard")
@login_required
def dashboard_main():
    type_dict = {
        Todo.TYPE_PLAN: "计划",
        Todo.TYPE_URGENT: "紧急",
        Todo.TYPE_PRIOR: "优先",
        Todo.TYPE_NORMAL: "普通", }
    type_style = {
        Todo.TYPE_PLAN: "label-success",
        Todo.TYPE_URGENT: "label-danger",
        Todo.TYPE_PRIOR: "label-primary",
        Todo.TYPE_NORMAL: "label-default", }
    _todos = Todo.query.search_date(timeutils.today(), timeutils.today()).filter(
        Todo.todo_status == Todo.STATUS_NOT_DONE).sort_by_type().all()
    _completeds = Todo.query.search_date(timeutils.today(), timeutils.today()).filter(
        Todo.todo_status == Todo.STATUS_DONE).sort_by_type().all()
    return render_template('admin/dashboard.html', todos=_todos, completeds=_completeds, type_dict=type_dict,
                           type_style=type_style)

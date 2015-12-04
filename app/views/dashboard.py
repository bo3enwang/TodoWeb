# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template
from app.models import Todo, Plan, Post, Image, db
from app import timeutils
from flask.ext.login import login_required
from sqlalchemy import func, and_
# import pylibmc as memcache

dashboard = Module(__name__)


# mc = memcache.Client()


@dashboard.route("")
@dashboard.route("/dashboard")
@login_required
def dashboard_main():
    if not mc.get('month_finish_plan'):
        month_finish_plan = db.session.query(func.count(Plan.id)).filter(
            and_(Plan.plan_end_date >= timeutils.get_firstday_month(),
                 Plan.plan_end_date <= timeutils.get_lastday_month(),
                 Plan.plan_status == Plan.STATUS_FINISH)).scalar()
        mc.set("month_finish_plan", month_finish_plan)

    if not mc.get('progress_plan'):
        progress_plan = db.session.query(func.count(Plan.id)).filter(
            Plan.plan_status == Plan.STATUS_PROGRESS).scalar()
        mc.set("progress_plan", progress_plan)

    if not mc.get('post_count'):
        post_count = db.session.query(func.count(Post.id)).scalar()
        mc.set("post_count", post_count)

    if not mc.get('img_count'):
        img_count = db.session.query(func.count(Image.id)).scalar()
        mc.set("img_count", img_count)
    overview_data = {
        'progress_plan': mc.get("progress_plan"),
        'month_finish_plan': mc.get("month_finish_plan"),
        'post_count': mc.get("post_count"),
        'img_count': mc.get("img_count"),
    }
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
                           type_style=type_style, overview_data=overview_data)

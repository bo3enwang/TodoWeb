# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template
from app.models import Todo, Plan, Post, Image, db
from app import timeutils
from flask.ext.login import login_required
from sqlalchemy import func, and_
from app.helps import cache


def _create_memcache_client():
    try:
        import pylibmc
        return pylibmc.Client()
    except ImportError:
        import memcache
        return memcache.Client(['127.0.0.1:11211'])


mem_cache = _create_memcache_client()

dashboard = Module(__name__)


@dashboard.route("")
@dashboard.route("/dashboard")
@login_required
@cache.cached(60)
def dashboard_main():
    if not mem_cache.get('month_finish_plan'):
        month_finish_plan = db.session.query(func.count(Plan.id)).filter(
            and_(Plan.plan_end_date >= timeutils.get_firstday_month(),
                 Plan.plan_end_date <= timeutils.get_lastday_month(),
                 Plan.plan_status == Plan.STATUS_FINISH)).scalar()
        mem_cache.set("month_finish_plan", month_finish_plan)

    if not mem_cache.get('progress_plan'):
        progress_plan = db.session.query(func.count(Plan.id)).filter(
            Plan.plan_status == Plan.STATUS_PROGRESS).scalar()
        mem_cache.set("progress_plan", progress_plan)

    if not mem_cache.get('post_count'):
        post_count = db.session.query(func.count(Post.id)).scalar()
        mem_cache.set("post_count", post_count)

    if not mem_cache.get('img_count'):
        img_count = db.session.query(func.count(Image.id)).scalar()
        mem_cache.set("img_count", img_count)
    overview_data = {
        'progress_plan': mem_cache.get("progress_plan"),
        'month_finish_plan': mem_cache.get("month_finish_plan"),
        'post_count': mem_cache.get("post_count"),
        'img_count': mem_cache.get("img_count"),
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

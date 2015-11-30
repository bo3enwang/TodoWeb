# -*- coding:utf8 -*-
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import db, Plan
from app.forms import PlanAddForm

plan = Module(__name__)


@plan.route("/plan/status/<string:plan_status>")
def plan_list(plan_status):
    status_num_dict = {
        "create": Plan.STATUS_CREATE,
        "progress": Plan.STATUS_PROGRESS,
        "finish": Plan.STATUS_FINISH,
    }
    if not status_num_dict.has_key(plan_status):
        return render_template('errors/404.html'), 404

    type_dict = {
        Plan.TYPE_LEARN: "学习",
        Plan.TYPE_READ: "阅读",
        Plan.TYPE_PROJECT: "项目",
        Plan.TYPE_OTHER: "其他",
    }
    plans = Plan.query.filter(Plan.plan_status == status_num_dict.get(plan_status)).all()
    form = PlanAddForm()

    return render_template("admin/planList.html", plans=plans, type_dict=type_dict, form=form, plan_status=plan_status)


@plan.route("/plan/add", methods=("post",))
def play_add():
    form = PlanAddForm()
    if form.validate_on_submit():
        p = Plan()
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        flash("新增计划成功", "success")
        return redirect(url_for("plan_list", plan_status="progress"))
    flash("新增计划失败", "success")
    return redirect(url_for("plan_list", plan_status="progress"))

# -*- coding:utf8 -*-
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import db, Plan, PlanRecord
from app.forms import PlanAddForm, PlanRecordForm

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
    add_form = PlanAddForm()
    record_form = PlanRecordForm()
    return render_template("admin/planList.html", plans=plans, type_dict=type_dict, add_form=add_form,
                           record_form=record_form, plan_status=plan_status)


@plan.route("/plan/add", methods=("post",))
def play_add():
    add_form = PlanAddForm()
    if add_form.validate_on_submit():
        p = Plan()
        add_form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        flash("新增计划成功", "success")
        return redirect(url_for("plan_list", plan_status="create"))
    flash("新增计划失败", "success")
    return redirect(url_for("plan_list", plan_status="create"))


@plan.route("/plan/record", methods=("post",))
def play_record():
    record_form = PlanRecordForm()
    if record_form.validate_on_submit():
        _plan = Plan.query.get_or_404(record_form.plan_id.data)
        if (record_form.record_point.data + _plan.plan_point) > _plan.plan_total:
            _plan.plan_status = Plan.STATUS_FINISH
        plan_record = PlanRecord()
        record_form.populate_obj(plan_record)
        db.session.add(plan_record)
        db.session.commit()
        flash("记录成功", "success")
        return redirect(url_for("plan_list", plan_status="progress"))
    flash("记录失败", "success")
    return redirect(url_for("plan_list", plan_status="progress"))


@plan.route("/plan/<int:plan_id>/delete/", methods=("post",))
def play_delete(plan_id):
    _plan = Plan.query.get_or_404(plan_id)
    db.session.delete(_plan)
    db.session.commit()
    flash("删除成功", "success")
    return jsonify(success=True,
                   redirect_url=url_for('plan_list', plan_status="progress"))


@plan.route("/plan/<int:plan_id>/activation/", methods=("post",))
def play_activation(plan_id):
    _plan = Plan.query.get_or_404(plan_id)
    _plan.plan_status = Plan.STATUS_PROGRESS
    db.session.commit()
    flash("激活成功", "success")
    return jsonify(success=True,
                   redirect_url=url_for('plan_list', plan_status="progress"))

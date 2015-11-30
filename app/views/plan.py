# -*- coding:utf8 -*-
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import db, Plan

plan = Module(__name__)


@plan.route('/plan')
@plan.route("/plan/<int:page>/")
def play_list(plan_type=0, page=1):
    # plans = Plan.query.all()
    # page_obj = Plan.query.sort_by_remain_day().base_info().paginate(page, per_page=10)
    return render_template("admin/planList.html")


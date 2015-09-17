# -*- coding:utf8 -*-
from flask.ext.login import login_required
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from app.forms import ProjectAddForm
from app.models import db, Project, ProjectHistory
from app import timeutils

project = Module(__name__)


@project.route('/p/data', methods=("post",))
def project_data():
    jsondata = request.get_json()
    pstatus = jsondata.get('pstatus')
    ptype = jsondata.get('ptype')
    statusDict = {
        "start": Project.STATUS_START,
        "progress": Project.STATUS_PROGRESS,
        "end": Project.STATUS_END,
    }
    pdata = Project.query.project_status(statusDict.get(pstatus)).restricted(g.user).jsonify()
    return jsonify({"result": pdata})


@project.route('/p/<pstatus>')
@login_required
def project_query(pstatus):
    form = ProjectAddForm()
    return render_template('project/project.html', form=form, pstatus=pstatus)


@project.route('/add', methods=("post",))
@login_required
def project_add():
    form = ProjectAddForm()
    result = -1
    if form.validate_on_submit():
        p = Project()
        p.p_all = form.p_all.data
        p.p_day = form.p_day.data
        p.type = form.type.data
        p.name = form.name.data
        p.user = g.user
        db.session.add(p)
        db.session.commit()
        result = 1
    return jsonify({'result': result})


@project.route('/begin', methods=("post",))
@login_required
def project_begin():
    jsondata = request.get_json()
    proid = jsondata.get('proid')
    p = Project.query.get(proid)
    result = -1
    if p.status == Project.STATUS_START:
        p.status = Project.STATUS_PROGRESS
        p.start_time = timeutils.today()
        p.end_time = timeutils.get_day_of_day(p.p_day)
        db.session.commit()
        result = 1

    return jsonify({'result': result})


# 新增计划进度
@project.route('/record', methods=("post",))
@login_required
def project_record():
    jsondata = request.get_json()
    result = -1
    proid = jsondata.get('proid')
    record = jsondata.get('record')
    if proid:
        ph = ProjectHistory()
        ph.record = record
        ph.project_id = proid
        db.session.add(ph)
        db.session.commit()
        result = proid
    return jsonify({'result': result})


@project.route('/delete', methods=("post",))
@login_required
def project_delete():
    result = -1
    jsondata = request.get_json()
    proid = jsondata.get('proid')
    p = Project.query.get_or_404(proid)
    if p:
        db.session.delete(p)
        db.session.commit()
        result = proid
    return jsonify({'result': result})

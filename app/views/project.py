from flask.ext.login import login_required
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify

from app.forms import ProjectAddForm
from app.models import db, Project,ProjectHistory
from app import timeutils

project = Module(__name__)


@project.route('/p/<ptype>')
@login_required
def project_query(ptype):
    if ptype == 'start':
        pjs = Project.query.start().restricted(g.user)
    elif ptype == 'progress':
        pjs = Project.query.progress().restricted(g.user)
    elif ptype == 'end':
        pjs = Project.query.end().restricted(g.user)
    else:
        pjs = Project.query.restricted(g.user).all()
    form = ProjectAddForm()
    return render_template('project/project.html', form=form, pjs=pjs)


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
        result = 1
    return jsonify({'result': result})

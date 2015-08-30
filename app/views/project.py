# # -*- coding:utf8 -*-
# __author__ = 'Zovven'
#
# from app import app, lm
# from app.models.projects import Project, ProjectHistory
# from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
# from flask.ext.login import login_user, logout_user, current_user, login_required
# from app.forms import LoginForm, AddProjectForm
# from datetime import datetime
# from app import db
# from app import utils
#
#
# @app.route('/project/add', methods=['POST'])
# def project_add():
#     addProjectform = AddProjectForm()
#     if addProjectform.validate_on_submit():
#         project = Project()
#         project.content = addProjectform.content.data
#         project.type = addProjectform.type.data
#         project.project_all = addProjectform.project_all.data
#         project.project_day = addProjectform.project_day.data
#         project.start_time = utils.today()
#         projectday = int(addProjectform.project_day.data)
#         end_time = utils.get_day_of_day(projectday)
#         project.end_time = end_time
#         project.user = current_user
#         db.session.add(project)
#         db.session.commit()
#     return redirect(url_for('myproject'))
#
#
# @app.route('/project')
# @login_required
# def myproject():
#     addProjectform = AddProjectForm()
#     projects = Project.query.filter_by(user=g.user).all()
#     return render_template('project.html', form=addProjectform, projects=projects)
#
#
# @app.route('/todo')
# @login_required
# def mytodo():
#     return render_template('todo.html')
#
#
# @app.route("/api/project/list")
# def api_project_list():
#     projects = Project.query.filter_by(user=g.user).all()
#     return jsonify(projects.jsonify())

from flask.ext.login import login_required
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify

from app.forms import ProjectAddForm
from app.models import db, Project
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
    a = form.p_all.data
    print a
    # if form.validate_on_submit():
        # p = Project()
        # p.p_all = form.p_all.data
        # p.p_day = form.p_day.data
        # p.type = form.type.data
        # p.name = form.name.data
        # p.user = g.user
        # db.session.add(p)
        # db.session.commit()
    return jsonify({'result': a})


@project.route('/begin', methods=("post",))
@login_required
def project_begin():
    jsondata = request.get_json()
    proid = jsondata.get('proid')
    p = Project.query.get(proid)
    if p.status == Project.STATUS_START:
        p.status = Project.STATUS_PROGRESS
        p.start_time = timeutils.today()
        p.end_time = timeutils.get_day_of_day(p.p_day)
        db.session.commit()
        result = 1
    else:
        result = -1

    return jsonify({'result': result})

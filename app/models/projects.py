# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import hashlib
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from users import User


class ProjectQuery(BaseQuery):
    def jsonify(self):
        for project in self.all():
            yield project.json


class Project(db.Model):
    query_class = ProjectQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.Integer)
    p_now = db.Column(db.Integer, default=0)
    p_all = db.Column(db.Integer)
    p_day = db.Column(db.Integer)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
    user = db.relation(User, innerjoin=True, lazy="joined")
    historys = db.relationship('ProjectHistory', backref='project', lazy='dynamic')

    @property
    def p_percent(self):
        percent = int((float(self.project_now) / float(self.project_all)) * 100)
        return percent

    @property
    def remain_days(self):
        print self.start_time
        print self.end_time
        timedelta = self.end_time - self.start_time
        return timedelta.days

    @cached_property
    def json(self):
        return dict(project_id=self.id,
                    content=self.content,
                    type=self.type,
                    project_now=self.project_now,
                    project_all=self.project_all,
                    project_day=self.project_day,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    user_id=self.user_id)


class ProjectHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    operate = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

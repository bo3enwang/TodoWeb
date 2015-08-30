# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import hashlib
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from users import User
from app import timeutils


class ProjectQuery(BaseQuery):
    def jsonify(self):
        for project in self.all():
            yield project.json

    def start(self):
        return self.filter(Project.status == Project.STATUS_START)

    def progress(self):
        return self.filter(Project.status == Project.STATUS_PROGRESS)

    def end(self):
        return self.filter(Project.status == Project.STATUS_END)

    def restricted(self, user=None):
        return self.filter(Project.user == user)


class Project(db.Model):
    query_class = ProjectQuery

    NORMAL = 1
    Priority = 5

    STATUS_START = 0
    STATUS_PROGRESS = 1
    STATUS_END = 2
    STATUS_DEAD = 3

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
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
        percent = int((float(self.p_now) / float(self.p_all)) * 100)
        return percent

    @property
    def remain_days(self):
        if self.start_time is not None and self.end_time is not None:
            timedelta = self.end_time - timeutils.today()
            if timedelta.days < 0:
                return -1
            return timedelta.days
        else:
            return 0

    @cached_property
    def json(self):
        return dict(p_id=self.id,
                    name=self.name,
                    type=self.type,
                    p_now=self.project_now,
                    p_all=self.project_all,
                    p_day=self.project_day,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    user_id=self.user_id)


class ProjectHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    operate = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

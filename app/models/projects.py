# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import json
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from users import User
from app import timeutils, jsonutil


class ProjectQuery(BaseQuery):
    def jsonify(self):
        jsonarry = []
        for project in self.all():
            jsonarry.append(project.json)
        return json.dumps(jsonarry, cls=jsonutil.TimeEncoder)

    def project_status(self, pstatus):
        return self.filter(Project.status == pstatus)

    def project_type(self, ptype):
        return self.filter(Project.type == ptype)

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

    TYPE_PROJECT = 0
    TYPE_READ = 1
    TYPE_SPORT = 2
    TYPE_LEARN = 3

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    p_all = db.Column(db.Integer)
    p_day = db.Column(db.Integer)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    user = db.relation(User, innerjoin=True, lazy="joined")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))

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
        return dict(id=self.id,
                    name=self.name,
                    type=self.type,
                    status=self.status,
                    p_now=self.p_now,
                    p_all=self.p_all,
                    remain_days=self.remain_days,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    user_id=self.user_id,
                    p_percent=self.p_percent)

    @cached_property
    def history(self):
        history = ProjectHistory.query.filter(ProjectHistory.project_id == self.id).all()
        return history

    @cached_property
    def p_now(self):
        count = 0
        for h in self.history:
            count += h.record
        return count


class ProjectHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.relation(Project, innerjoin=True, lazy="joined")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))
    record = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

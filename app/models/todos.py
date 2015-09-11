# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import json
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from sqlalchemy import and_
from users import User
from app import timeutils, jsonutil


class TodoQuery(BaseQuery):
    def jsonify(self):
        jsonarry = []
        for project in self.all():
            jsonarry.append(project.json)
        return json.dumps(jsonarry, cls=jsonutil.TimeEncoder)

    def query_day(self, t_date):
        return self.filter(Todo.t_date == t_date)

    def restricted(self, user=None):
        return self.filter(Todo.user == user)


class Todo(db.Model):
    query_class = TodoQuery

    STATUS_DONE = 1
    STATUS_NOT_DONE = 0

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    t_date = db.Column(db.Date)
    status = db.Column(db.Integer, default=0)
    user = db.relation(User, innerjoin=True, lazy="joined")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))

    @cached_property
    def json(self):
        return dict(id=self.id,
                    name=self.name,
                    t_date=self.t_date,
                    status=self.status,
                    user_id=self.user_id)

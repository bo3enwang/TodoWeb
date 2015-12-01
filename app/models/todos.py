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
    # def jsonify(self):
    #     jsonarry = []
    #     for project in self.all():
    #         jsonarry.append(project.json)
    #     return json.dumps(jsonarry, cls=jsonutil.TimeEncoder)

    def query_day(self, t_date):
        return self.filter(Todo.t_date == t_date)

    def restricted(self, user=None):
        return self.filter(Todo.user == user)


class Todo(db.Model):
    query_class = TodoQuery

    STATUS_DONE = 1
    STATUS_NOT_DONE = 0

    TYPE_URGENT_IMPORTANT = 1
    TYPE_URGENT = 2
    TYPE_IMPORTANT = 3
    TYPE_NONE = 4

    id = db.Column(db.Integer, primary_key=True)
    todo_desc = db.Column(db.String(80))
    todo_date = db.Column(db.Date)
    todo_status = db.Column(db.Integer, default=0)
    todo_type = db.Column(db.Integer, default=4)
    todo_time = db.Column(db.Integer)
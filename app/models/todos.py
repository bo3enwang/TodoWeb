# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import json
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from sqlalchemy import and_
from app import timeutils, jsonutil


class TodoQuery(BaseQuery):
    def jsonify(self):
        for post in self.all():
            yield post.json

    def search_date(self, start_date, end_date):
        return self.filter(and_(Todo.todo_date >= start_date, Todo.todo_date <= end_date))

    def sort_by_type(self):
        return self.order_by(Todo.todo_type.asc())


class Todo(db.Model):
    query_class = TodoQuery

    STATUS_DONE = 1
    STATUS_NOT_DONE = 0

    TYPE_PLAN = 0
    TYPE_URGENT = 1
    TYPE_PRIOR = 2
    TYPE_NORMAL = 3

    id = db.Column(db.Integer, primary_key=True)
    todo_desc = db.Column(db.String(80))
    todo_date = db.Column(db.Date, default=date.today())
    todo_status = db.Column(db.Integer, default=0)
    todo_type = db.Column(db.Integer, default=3)
    todo_time = db.Column(db.Integer)

    @cached_property
    def json_date(self):
        return self.todo_date.strftime('%Y-%m-%d')

    @cached_property
    def json(self):
        return dict(id=self.id,
                    todo_desc=self.todo_desc,
                    todo_status=self.todo_status,
                    todo_type=self.todo_type,
                    todo_date=self.json_date,
                    todo_time=self.todo_time)

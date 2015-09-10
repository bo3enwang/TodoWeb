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
        return None

    def day(self, t_date):
        return self.filter(Todo.t_date == t_date)

    def restricted(self, user=None):
        return self.filter(Todo.user == user)


class Todo(db.Model):
    query_class = TodoQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    t_date = db.Column(db.Date)
    status = db.Column(db.Integer)
    user = db.relation(User, innerjoin=True, lazy="joined")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))

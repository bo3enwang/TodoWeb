# -*- coding:utf8 -*-
__author__ = 'Zovven'

from app import db
import hashlib
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    nickname = db.Column(db.String(80))
    last_seen = db.Column(db.DateTime)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def get_auth_token(self):
        m = hashlib.md5(self.username)
        return m.hexdigest()

    def __repr__(self):
        return '<User %r>' % self.nickname


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80))
    type = db.Column(db.Integer)
    task_now = db.Column(db.Integer)
    task_all = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    historys = db.relationship('TaskHistory', backref='task', lazy='dynamic')


class TaskHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    operate = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

# -*- coding:utf8 -*-
__author__ = 'Zovven'

from app import db
import hashlib
from datetime import date, datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    nickname = db.Column(db.String(80))
    last_seen = db.Column(db.DateTime)

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


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80))
    type = db.Column(db.Integer)
    project_now = db.Column(db.Integer, default=0)
    project_all = db.Column(db.Integer)
    project_day = db.Column(db.Integer)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
    user = db.relation(User, innerjoin=True, lazy="joined")
    historys = db.relationship('ProjectHistory', backref='project', lazy='dynamic')

    @property
    def project_percent(self):
        percent = int((float(self.project_now) / float(self.project_all)) * 100)
        return percent

    @property
    def remain_days(self):
        print self.start_time
        print self.end_time
        timedelta = self.end_time - self.start_time
        return timedelta.days


class ProjectHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    operate = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

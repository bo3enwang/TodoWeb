# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from app import db
import hashlib
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery


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

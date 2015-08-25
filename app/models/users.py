# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import hashlib
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from werkzeug.utils import cached_property
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import BaseQuery


class UserQuery(BaseQuery):
    def authenticate(self, login, password):

        user = self.filter(db.or_(User.username == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated


class User(db.Model):
    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    nickname = db.Column(db.String(80))
    last_seen = db.Column(db.DateTime)

    _password = db.Column("password", db.String(80))

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

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))

    def __repr__(self):
        return '<User %r>' % self.nickname

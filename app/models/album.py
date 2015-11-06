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


class AlbumQuery(BaseQuery):
    def sort_by_date(self):
        return self.order_by(Album.upload_date.desc())

    def as_list(self):
        """
        Return restricted list of columns for list queries
        """
        deferred_cols = ("img_url",
                         "img_name")
        options = [db.defer(col) for col in deferred_cols]
        return self.options(*options)


class Album(db.Model):

    TYPE_PRIVATE = 0
    TYPE_PUBLIC = 1

    query_class = AlbumQuery
    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    img_key = db.Column(db.String(255))
    type = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.DateTime, default=datetime.now)

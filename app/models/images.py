# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from ._base import db
from flask_sqlalchemy import BaseQuery

from datetime import date, datetime, timedelta


class AlbumQuery(BaseQuery):
    def sort_by_date(self):
        return self.order_by(Image.upload_date.desc())

    def as_list(self):
        """
        Return restricted list of columns for list queries
        """
        deferred_cols = ("img_url",
                         "img_name")
        options = [db.defer(col) for col in deferred_cols]
        return self.options(*options)


class Image(db.Model):
    TYPE_PRIVATE = 0
    TYPE_PUBLIC = 1

    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    img_key = db.Column(db.String(255))
    img_type = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.DateTime, default=datetime.now)

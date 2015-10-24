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


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    img_key = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

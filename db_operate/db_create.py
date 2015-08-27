# -*- coding:utf8 -*-
__author__ = 'Zovven'
#创建数据库

from app import create_app
from app.models import db
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import create_app
import os.path
app = create_app()
db.app = app
db.init_app(app)
db.create_all()

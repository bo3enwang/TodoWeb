# -*- coding:utf8 -*-
__author__ = 'Zovven'
#创建数据库

from app.models import db
from app import create_app

app = create_app()
db.app = app
db.init_app(app)
# db.create_all()

# db = create_db()
db.create_all()

print(1)

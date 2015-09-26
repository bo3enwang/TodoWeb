# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask.ext.sqlalchemy import SQLAlchemy


class nullpool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(nullpool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        from sqlalchemy.pool import NullPool
        options['poolclass'] = NullPool
        del options['pool_size']


# db = nullpool_SQLAlchemy()
db = SQLAlchemy()


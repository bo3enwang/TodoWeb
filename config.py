# -*- coding:utf8 -*- 
__author__ = 'Zovven'
import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))

MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
MYSQL_DB = 'todoweb'

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
                          % (MYSQL_USER, MYSQL_PASS,
                             MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

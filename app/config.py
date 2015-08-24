# -*- coding:utf8 -*- 
__author__ = 'Zovven'
import os


class DefaultConfig(object):
    DEBUG = True

    # change this in your production settings !!!

    SECRET_KEY = "do_not_guess"
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

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 30

    # # 需要测试发送邮件功能的时候，自由设置！
    # # 如果需要开启代码中向管理员发送邮件的功能的话，需要在 ADMINS 里面添加收件人
    # # 如: ADMINS = ('admin@newsmeme.com')。默认情况下这个功能关闭
    # ADMINS = ()
    #
    # MAIL_SERVER = u'smtp.qq.com'
    # MAIL_USERNAME = u'920863755@qq.com'
    # MAIL_PASSWORD = u'wbw1992'
    # DEFAULT_MAIL_SENDER = u'smtp.qq.com'
    #
    # ACCEPT_LANGUAGES = ['en', 'fi']
    #
    # DEBUG_LOG = 'logs/debug.log'
    # ERROR_LOG = 'logs/error.log'
    #
    # CACHE_TYPE = "simple"
    # CACHE_DEFAULT_TIMEOUT = 300


class TestConfig(object):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False

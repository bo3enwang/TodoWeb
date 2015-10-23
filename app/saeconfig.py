# -*- coding:utf8 -*- 
__author__ = 'Zovven'

import sae.const


class DefaultConfig(object):
    DEBUG = False

    # change this in your production settings !!!

    SECRET_KEY = "6L+Z5bCx5piv5oiRLFpvdnZlbg=="

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'root'
    MYSQL_PASS = 'root'
    MYSQL_DB = 'todoweb'

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
                              % (sae.const.MYSQL_USER, sae.const.MYSQL_PASS,
                                 sae.const.MYSQL_HOST, sae.const.MYSQL_PORT, sae.const.MYSQL_DB)

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 30


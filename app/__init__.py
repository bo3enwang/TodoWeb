# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Flask, request, url_for, g, render_template, flash
import os
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'

db = SQLAlchemy(app)

from app import models,views

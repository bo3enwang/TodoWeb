# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from ._base import lm

home = Module(__name__)


@home.route("/")
def home_index():
    # flash('hehe')
    # return render_template("home/post.html")
    return redirect(url_for('home.blog_view'))


@home.route("/blog")
def blog_view():
    return render_template("home/base.html")

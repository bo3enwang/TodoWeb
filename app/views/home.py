# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import db, Post

from ._base import lm

home = Module(__name__)


@home.route("/")
def home_index():
    return redirect(url_for('home.blog_list'))


@home.route("/back")
def admin_index():
    return redirect(url_for('todo.index'))


@home.route("/blog")
@home.route("/blog/<int:page>/")
def blog_list(page=1):
    page_obj = Post.query.sort_by_date().just_title().paginate(page, per_page=2)
    return render_template("home/blog.html", page_obj=page_obj)

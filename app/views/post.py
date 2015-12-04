# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask.ext.login import login_required
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from app.forms import PostForm
from app.models import db, Post, Tag
from app import timeutils

post = Module(__name__)


@post.route('')
@login_required
def post_list():
    posts = Post.query.all()
    return render_template('admin/postList.html', posts=posts)


@post.route("/<int:post_id>/edit/", methods=("GET", "POST"))
@login_required
def post_edit(post_id):
    p = Post.query.get_or_404(post_id)
    form = PostForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash("更新文章成功", "success")
        return redirect(url_for("post.post_list"))

    return render_template('admin/postEdit.html', post=p, form=form, acurl="/admin/post/" + str(post_id) + "/edit/")


@post.route("/add", methods=("GET", "POST"))
@login_required
def post_add():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(user=g.user)
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        flash("新增文章成功", "success")
        return redirect(url_for("post_list"))
    return render_template("admin/postEdit.html", form=form, acurl='/admin/post/add')


@post.route("/<int:post_id>/delete/", methods=("POST",))
@login_required
def delete(post_id):
    p = Post.query.get_or_404(post_id)
    db.session.delete(p)
    db.session.commit()
    d = db.delete(Tag, Tag.num_posts == 0)
    db.engine.execute(d)
    flash("删除文章成功", "success")
    return jsonify(success=True,
                   redirect_url=url_for('post.post_list'))

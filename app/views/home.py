# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Module, render_template, redirect, url_for
from app.models import Post, Tag, Image

home = Module(__name__)


@home.route("/")
def home_index():
    return redirect(url_for('home.blog_list'))


@home.route("/blog")
@home.route("/blog/<int:page>/")
def blog_list(page=1):
    tags = Tag.query.filter(Tag.num_posts > 0).all()
    page_obj = Post.query.sort_by_date().just_title().paginate(page, per_page=10)
    return render_template("home/blog.html", page_obj=page_obj, tags=tags)


@home.route("/post/<int:post_id>/")
def blog_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("home/postview.html", post=post)


@home.route("/tags/")
def tag_list():
    tags = Tag.query.filter(Tag.num_posts > 0).all()
    return render_template("home/tags.html", tags=tags)


@home.route("/tags/<slug>/")
@home.route("/tags/<slug>/<int:page>/")
def tag_view(slug, page=1):
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page_obj = tag.posts.sort_by_date().just_title().paginate(page, per_page=8)
    tags = Tag.query.filter(Tag.num_posts > 0).all()
    return render_template("home/tag.html", tag=tag, page_obj=page_obj, tags=tags)


@home.route("/album")
@home.route("/album/<int:page>/")
def album_list(page=1):
    page_obj = Image.query.filter(Image.type > 0).sort_by_date().as_list().paginate(page, per_page=6)
    return render_template("home/album.html", page_obj=page_obj)


@home.route("/about")
def about_me():
    return render_template("home/about.html")

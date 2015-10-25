# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import json
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from users import User
from app.tocutil import TocRenderer
from app import timeutils, jsonutil
import mistune
from app.helps import slugify


class PostQuery(BaseQuery):
    def search(self, keywords):
        criteria = []

        for keyword in keywords.split():
            keyword = '%' + keyword + '%'

            criteria.append(db.or_(Post.title.ilike(keyword),
                                   Post.tags.ilike(keyword),
                                   User.username.ilike(keyword)))

        q = reduce(db.and_, criteria)

        return self.filter(q).join(User).distinct()

    def just_title(self):
        """
        Return restricted list of columns for list queries
        """
        deferred_cols = ("date_created",
                         "title")
        options = [db.defer(col) for col in deferred_cols]
        return self.options(*options)

    def sort_by_date(self):
        return self.order_by(Post.date_created.desc())


class Post(db.Model):
    __tablename__ = "posts"
    query_class = PostQuery

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
    content = db.Column(db.UnicodeText)
    user = db.relation(User, innerjoin=True, lazy="joined")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    _tags = db.Column("tags", db.UnicodeText)

    def _get_tags(self):
        return self._tags

    def _set_tags(self, tags):

        self._tags = tags

        if self.id:
            # ensure existing tag references are removed
            d = db.delete(post_tags, post_tags.c.post_id == self.id)
            db.engine.execute(d)
            db.session.commit()

        for tag in set(self.taglist):
            slug = slugify(tag)
            tag_obj = Tag.query.filter(Tag.slug == slug).first()

            if tag_obj is None:
                tag_obj = Tag(name=tag)
                db.session.add(tag_obj)

            if self not in tag_obj.posts:
                tag_obj.posts.append(self)

    tags = db.synonym("_tags", descriptor=property(_get_tags, _set_tags))

    @cached_property
    def markdown(self):
        toc = TocRenderer()
        toc.reset_toc()  # initial the status
        md = mistune.Markdown(renderer=toc)
        return md(self.content or '')

    @cached_property
    def toc(self):
        toc = TocRenderer()
        toc.reset_toc()  # initial the status
        md = mistune.Markdown(renderer=toc)
        md.parse(self.content or '')
        return toc.render_toc()

    @property
    def taglist(self):
        if self.tags is None:
            return []

        tags = [t.strip() for t in self.tags.split(",")]
        return [t for t in tags if t]


post_tags = db.Table("post_tags", db.Model.metadata,
                     db.Column("post_id", db.Integer,
                               db.ForeignKey('posts.id', ondelete='CASCADE'),
                               primary_key=True),

                     db.Column("tag_id", db.Integer,
                               db.ForeignKey('tags.id', ondelete='CASCADE'),
                               primary_key=True))


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode(80), unique=True)
    posts = db.dynamic_loader(Post, secondary=post_tags, query_class=PostQuery)
    _name = db.Column("name", db.Unicode(80), unique=True)

    def __str__(self):
        return self.name

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name.lower().strip()
        self.slug = slugify(name)

    name = db.synonym("_name", descriptor=property(_get_name, _set_name))

    num_posts = db.column_property(
        db.select([db.func.count(post_tags.c.post_id)]).where(
            db.and_(post_tags.c.tag_id == id, Post.id == post_tags.c.post_id)).as_scalar())

__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User, Project, ProjectHistory, Todo, Post, Tag, post_tags, Album
import json
from app.jsonutil import TimeEncoder
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import timeutils

manager = Manager(create_app())


@manager.command
def saveuser():
    user = User(username='zo', email='ewq@qq.com')
    user.password = '123'
    db.session.add(user)
    db.session.commit()
    db.session.close()


@manager.command
def bathaddp():
    user = User.query.get(1)
    for i in range(10):
        p = Project()
        p.user = user
        p.name = "ehhe" + str(i)
        p.p_all = 50 + i * 10
        p.p_day = 3 + i * 3
        db.session.add(p)
        db.session.commit()


@manager.command
def bathaddto():
    user = User.query.get(1)
    for i in range(20):
        t = Todo()
        t.user = user
        t.t_date = timeutils.today()
        t.name = "ehhe" + str(i)
        db.session.add(t)
        db.session.commit()


@manager.command
def findp():
    user = User.query.get(1)
    print user.id
    pjs = Project.query.start().restricted(user)
    for p in pjs:
        print p.name


@manager.command
def qpj():
    user = User.query.get(1)
    jsondata = Project.query.progress().restricted(user).jsonify()
    print json.dumps(jsondata, cls=TimeEncoder)


@manager.command
def ph():
    project = Project.query.first()
    ph = ProjectHistory()
    ph.project = project
    ph.progress = 55
    db.session.add(ph)
    db.session.commit()


@manager.command
def addtodo():
    user = User.query.get(1)
    todo = Todo()
    todo.user = user
    todo.name = "hehehehe"
    todo.t_date = timeutils.today()
    todo.status = 0
    db.session.add(todo)
    db.session.commit()


@manager.command
def addPost():
    user = User.query.get(1)
    for x in range(10):
        post = Post()
        post.user = user
        post.tags = 'java,ruby'
        post.title = 'test' + str(x)
        post.content = '#bad'
        db.session.add(post)
    db.session.commit()


@manager.command
def queryPost():
    # page_obj = Post.query.sort_by_date().just_title().paginate(1, per_page=3)
    # print page_obj.page
    # for p_num in range(page_obj.pages):
    #     print p_num
    # tags = db.session.query_property(Post)
    # for tag in tags:
    #     print tag.name
    post = Post.query.first()
    for x in post.linked_taglist:
        print x[0]


@manager.command
def add_album():
    al = Album(img_name="testpic-1", img_url='http://zovven-zovvenimage.stor.sinaapp.com/249006-106.jpg')
    db.session.add(al)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

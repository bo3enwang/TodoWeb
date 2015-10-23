__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User, Project, ProjectHistory, Todo, Post, Tag, post_tags
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
def ph():
    t_date = '2015-09-13'
    tododata = Todo.query.query_day(t_date).restricted(g.user).jsonify()


@manager.command
def addPost():
    post = Post()
    user = User.query.get(1)
    post.user = user
    post.tags = 'java,ruby'
    post.title = '2 test'
    post.content = '#bad'
    db.session.add(post)
    db.session.commit()


@manager.command
def queryPost():
    d = db.delete(Tag, Tag.num_posts == 0)
    db.engine.execute(d)


if __name__ == '__main__':
    manager.run()

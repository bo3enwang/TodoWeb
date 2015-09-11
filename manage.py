__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User, Project, ProjectHistory, Todo
import json
from app.jsonutil import TimeEncoder
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import timeutils

manager = Manager(create_app())


@manager.command
def saveuser():
    user = User(username='zo', email='bluewbw@qq.com')
    user._set_password('123')
    db.session.add(user)
    db.session.commit()
    db.session.close()


@manager.command
def dopw():
    user, authenticated = User.query.authenticate('zo', '123')
    print user.email
    print authenticated


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


if __name__ == '__main__':
    manager.run()

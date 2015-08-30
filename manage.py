__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User, Project
import json
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
    project = Project.query.first()
    print timeutils.today()
    project.start_time = timeutils.today()
    db.session.commit()


if __name__ == '__main__':
    manager.run()

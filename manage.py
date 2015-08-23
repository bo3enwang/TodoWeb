__author__ = 'Zovven'
from flask.ext.script import Manager
from app import app
from app import db
from app.models.users import User
from app.models.projects import Project
import json
from flask import jsonify

manager = Manager(app)


@manager.command
def saveuser():
    user = User(username='zo', password='123')
    db.session.add(user)
    db.session.commit()
    db.session.close()


@manager.command
def queryproject():
    projects = Project.query.jsonify()
    print projects


if __name__ == '__main__':
    manager.run()

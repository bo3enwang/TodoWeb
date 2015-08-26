__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User
import json
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

manager = Manager(create_app())


@manager.command
def saveuser():
    user = User(username='zo',email='bluewbw@qq.com')
    user._set_password('123')
    db.session.add(user)
    db.session.commit()
    db.session.close()

@manager.command
def dopw():
    user, authenticated = User.query.authenticate('zo', '123')
    print user.email
    print authenticated



# @manager.command
# def queryproject():
#     # projects = Project.query.jsonify()
#     # print projects
#     project = Project.query.first()
#     print project.project_percent
#
#



if __name__ == '__main__':
    manager.run()

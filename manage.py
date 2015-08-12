__author__ = 'Zovven'
from flask.ext.script import Manager
from app import app
from app import db
from app.models import User, Project

manager = Manager(app)


@manager.command
def saveuser():
    user = User(username='zo', password='123')
    db.session.add(user)
    db.session.commit()
    db.session.close()


@manager.command
def queryproject():
    project = Project.query.first()
    print project.project_percent


if __name__ == '__main__':
    manager.run()

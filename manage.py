__author__ = 'Zovven'
from flask.ext.script import Manager
from app import app
from app import db
from app.models import User

manager = Manager(app)

@manager.command
def saveUser():
    user = User(username='zo',password='123')
    db.session.add(user)
    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    manager.run()
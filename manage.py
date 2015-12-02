__author__ = 'Zovven'
from flask.ext.script import Manager
from app import create_app
from app.models import db
from app.models import User, Project, ProjectHistory, Todo, Post, Tag, post_tags, Album, PlanRecord, Plan
import json
from app.jsonutil import TimeEncoder
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import timeutils
from sqlalchemy import func
from datetime import date, datetime, timedelta
import random

manager = Manager(create_app())


@manager.command
def add_plan():
    for x in range(20):
        plan = Plan()
        plan.plan_name = 'test plan' + str(x)
        plan.plan_day = random.randint(3, 999)
        plan.plan_total = random.randint(10, 9999)
        db.session.add(plan)
    db.session.commit()


@manager.command
def add_plan_record():
    plans = Plan.query.filter(Plan.id > 6).all()
    for plan in plans:
        for x in range(random.randint(1, 6)):
            plan_record = PlanRecord()
            plan_record.plan = plan
            plan_record.record_point = x * random.randint(1, 11)
            db.session.add(plan_record)
    db.session.commit()


@manager.command
def change_plan():
    plans = Plan.query.all()
    for plan in plans:
        plan.plan_type = random.randint(0, 3)
    db.session.commit()


@manager.command
def query_plan_num():
    _plan = Plan.query.filter(Plan.id == 1).first()
    # a = db.session.query(func.sum(PlanRecord.record_point)).filter(PlanRecord.plan_id == 2).scalar()
    print _plan.plan_total


@manager.command
def add_todo():
    for x in range(10):
        todo = Todo()
        todo.todo_desc = 'test plan--' + str(x) + str(x) + str(x)
        todo.todo_status = random.randint(0, 1)
        todo.todo_type = random.randint(1, 3)
        db.session.add(todo)
    db.session.commit()


@manager.command
def query_todo():
    todos = Todo.query.search_date(date.today(), date.today())
    print list(todos.jsonify())


if __name__ == '__main__':
    manager.run()

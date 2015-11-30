# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from ._base import db
import json
from sqlalchemy import func
from datetime import date, datetime, timedelta
from werkzeug.utils import cached_property
from flask_sqlalchemy import BaseQuery
from sqlalchemy import and_
from users import User
from app import timeutils, jsonutil


class PlanQuery(BaseQuery):
    def base_info(self):
        """
        Return restricted list of columns for list queries
        """
        deferred_cols = ("id",
                         "plan_type",
                         "plan_name",
                         "plan_percent",
                         "plan_point",
                         "plan_total",
                         "plan_remain_day")
        options = [db.defer(col) for col in deferred_cols]
        return self.options(*options)

    def sort_by_remain_day(self):
        return self.order_by(Plan.plan_remain_day.asc())


class Plan(db.Model):
    TYPE_LEARN = 0
    TYPE_READ = 1
    TYPE_PROJECT = 2
    TYPE_OTHER = 3

    STATUS_CREATE = 0
    STATUS_PROGRESS = 1
    STATUS_FINISH = 2

    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(80))
    plan_day = db.Column(db.Integer)
    plan_total = db.Column(db.Integer)

    plan_type = db.Column(db.Integer, default=0)
    plan_status = db.Column(db.Integer, default=0)

    plan_start_date = db.Column(db.Date)
    plan_end_date = db.Column(db.Date)

    @property
    def plan_remain_day(self):
        if self.plan_status != Plan.STATUS_PROGRESS or self.plan_start_date is None or self.plan_day is None:
            return 0
        remain_day = self.plan_day - (timeutils.today() - self.plan_start_date).days
        return remain_day

    @property
    def plan_point(self):
        return db.session.query(func.sum(PlanRecord.record_point)).filter(PlanRecord.plan_id == self.id).scalar() or 0

    @property
    def plan_percent(self):
        percent = int((float(self.plan_point) / float(self.plan_total)) * 100)
        return percent

    @property
    def plan_records(self):
        records = PlanRecord.query.filter(PlanRecord.plan_id == self.id).all()
        return records


class PlanRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan = db.relation(Plan, innerjoin=True, lazy="joined")
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id', ondelete='CASCADE'))
    record_date = db.Column(db.Date)
    record_point = db.Column(db.Integer)

# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class PlanAddForm(Form):
    plan_type = IntegerField("计划类型", validators=[NumberRange(min=0, max=5)])

    plan_name = StringField("计划名", validators=[DataRequired(), Length(min=1, max=30)])

    plan_total = IntegerField("计划总长", validators=[DataRequired(), NumberRange(min=10, max=9999)])

    plan_day = IntegerField("计划完成天数", validators=[DataRequired(), NumberRange(min=3, max=999)])


class PlanRecordForm(Form):
    plan_id = IntegerField("计划ID", validators=[DataRequired()])
    record_point = IntegerField("记录点数", validators=[DataRequired()])

# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class PlanAddForm(Form):
    plan_type = IntegerField("Project type", validators=[NumberRange(min=0, max=5)])

    plan_name = StringField("Project name", validators=[DataRequired(), Length(min=1, max=30)])

    plan_total = IntegerField("Project length", validators=[DataRequired(), NumberRange(min=10, max=9999)])

    plan_day = IntegerField("Project day", validators=[DataRequired(), NumberRange(min=3, max=999)])
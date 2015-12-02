# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField, \
    DateField
from wtforms.validators import DataRequired, Length, NumberRange


class TodoAddForm(Form):
    todo_type = IntegerField("Todo 类型", validators=[NumberRange(min=0, max=5)])
    todo_desc = StringField("Todo 描述", validators=[DataRequired(), Length(min=1, max=30)])


class TodoCompeteForm(Form):
    todo_id = IntegerField("Todo Id", validators=[DataRequired()])
    todo_time = IntegerField("Todo 用时", validators=[NumberRange(min=1, max=1200)])

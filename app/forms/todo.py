# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField, \
    DateField
from wtforms.validators import DataRequired, Length, NumberRange


class TodoAddForm(Form):
    t_date = DateField("Todo Date", validators=[DataRequired()])
    name = StringField("Todo name", validators=[DataRequired(), Length(min=1, max=30)])

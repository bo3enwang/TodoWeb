# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    next = HiddenField()

    remember = BooleanField(("Remember me"))

    login = StringField(("Username or Email address"), validators=[DataRequired()])

    password = PasswordField(("Password"), validators=[DataRequired()])

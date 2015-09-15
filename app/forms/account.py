# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User


class LoginForm(Form):
    remember = BooleanField("Remember me")

    login = StringField("Username or Email address", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField("用户名", validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = StringField("密码", validators=[DataRequired(), Length(min=1, max=30), EqualTo('confirm', "两次密码必须相同")])
    confirm = StringField("重复密码")

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).count() > 0:
            raise ValueError('邮箱已被使用')

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).count() > 0:
            raise ValueError('用户名已被使用')

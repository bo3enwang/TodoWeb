# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField, \
    TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class PostForm(Form):
    title = StringField("title", validators=[DataRequired(), Length(min=1, max=80)])
    content = TextAreaField("content", validators=[DataRequired()])
    tags = TextAreaField("content", validators=[DataRequired()])

# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask.ext.wtf import Form
from wtforms import TextAreaField, BooleanField, TextField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
from app import db
from app.models import User


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = TextField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def validate_login(self):
        user = self.get_user()
        login_info = {"result": "1", "msg": "login success"}
        if user is None:
            login_info["result"] = 0
            login_info["msg"] = "用户名或密码错误"
            return login_info

        if user.password != self.password.data:
            login_info["result"] = 0
            login_info["msg"] = "用户名或密码错误"
            return login_info

        return login_info

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()


class AddTaskForm(Form):
    content = TextField('任务内容', validators=[DataRequired()])
    type = TextField('任务优先级', validators=[DataRequired()])
    task_all = TextField('进度总长', validators=[DataRequired()])
    start_time = TextField('开始日期', validators=[DataRequired()])
    end_time = TextField('结束日期', validators=[DataRequired()])
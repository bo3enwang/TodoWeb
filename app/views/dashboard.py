# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify

dashboard = Module(__name__)


@dashboard.route("")
@dashboard.route("/dashboard")
def dashboard_main():
    return render_template('admin/dashboard.html')

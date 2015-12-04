# -*- coding:utf8 -*- 
__author__ = 'Zovven'

import sys
import views
from localconfig import DefaultConfig
from flask import Flask, request, g, jsonify, redirect, url_for, flash, render_template
from app import views



# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

DEFAULT_APP_NAME = "app"

DEFAULT_MODULES = (
    (views.home, ""),
    (views.account, "/admin/account"),
    (views.dashboard, "/admin"),
    (views.plan, "/admin/plan"),
    (views.todo, "/admin/todo"),
    (views.post, "/admin/post"),
    (views.image, "/admin/image"),
)


def create_db():
    from .models import db
    db.init_app(create_app())
    return db


def create_app(config=None, app_name=None, modules=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)

    configure_app(app, config)
    configure_errorhandlers(app)
    configure_modules(app, modules)
    configure_g_user(app)
    register_db(app)
    register_lm(app)
    return app


def configure_app(app, config):
    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

        # app.config.from_envvar('APP_CONFIG', silent=True)


def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)


def register_db(app):
    from .models import db
    db.init_app(app)


def register_lm(app):
    from views._base import lm
    lm.init_app(app)


def configure_g_user(app):
    from flask_login import current_user

    @app.before_request
    def before_request():
        g.user = current_user


def configure_errorhandlers(app):
    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error='Sorry, page not found')
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error='Sorry, not allowed')
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error='Sorry, an error has occurred')
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error="Login required")
        flash("Please login to see this page", "error")
        return redirect(url_for("account.login", next=request.path))

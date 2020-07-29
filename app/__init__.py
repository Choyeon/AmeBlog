# @Time    : 2020/7/28 3:09 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : __init__.py
import os

from flask import Flask, render_template

from app.blueprints.admin import admin_bp
from app.blueprints.auth import auth_bp
from app.blueprints.blog import blog_bp
from app.extensions import bootstrap, db, ckeditor, mail, moment
from app.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask('Ameblog')
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    return app


def register_logging(app):
    # 注册日志
    pass


def register_extensions(app):
    # 注册flask扩展
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_commands(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    ...


def register_shell_context(app):
    pass


def register_template_context(app):
    pass

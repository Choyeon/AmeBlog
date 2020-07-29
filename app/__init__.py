# @Time    : 2020/7/28 3:09 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : __init__.py
import os

from flask import Flask

from app.blueprints.blog import blog_bp
from app.settings import config


def create_app(config_name=None):
    if config is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Ameblog')
    app.config.from_object(config[config_name])

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app

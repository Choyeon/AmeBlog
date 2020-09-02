# @Time    : 2020/7/28 3:09 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : __init__.py
import os
import click
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from app.blueprints.admin import admin_bp
from app.blueprints.auth import auth_bp
from app.blueprints.blog import blog_bp
from app.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate
from app.fakes import fake_links
from app.models import Admin, Post, Category, Comment, Link
from app.settings import config, basedir


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask('app')
    app.config.from_object(config[config_name])


    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)
    return app


def register_logging(app):
    # 注册日志
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/app.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='app Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_extensions(app):
    # 注册flask扩展
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    # app.config['WTF_I18N_ENABLED'] = False


def register_blueprints(app):
    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除后创建。')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('此操作将删除数据库，您要继续吗？', abort=True)
            db.drop_all()
            click.echo('删除表。')
        db.create_all()
        click.echo('初始化的数据库。')

    @app.cli.command()
    @click.option('--username', prompt=True, help='用于登录的用户名。')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='登录密码。')
    def init(username, password):

        click.echo('初始化数据库...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('管理员已经存在，正在更新...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('正在创建临时管理员帐户...')
            admin = Admin(
                username=username,
                blog_title='AmeBlog',
                blog_sub_title="Hello world",
                name='Admin',
                about='Hello world'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('正在创建默认类别...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('完成.')

    @app.cli.command()
    @click.option('--category', default=10, help='生成分类数量，默认为10。')
    @click.option('--post', default=50, help='生成文章数量，默认为50。')
    @click.option('--comment', default=500, help='生成评论数量，默认为500。')
    def forge(category, post, comment):
        """
        生成伪造的分类，帖子和评论
        """
        from .fakes import fake_category, fake_posts, fake_comments, fake_admin
        db.drop_all()
        db.create_all()
        click.echo('正在生成管理员账号')
        fake_admin()
        click.echo('正在生成%d个分类' % category)
        fake_category(category)
        click.echo('正在生成%d个文章' % post)
        fake_posts(post)
        click.echo('正在生成%d个评论' % comment)
        fake_comments(comment)
        click.echo('正在生成links...')
        fake_links()
        click.echo('完成')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories,
            links=links, unread_comments=unread_comments)


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['AMEBLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response

# @Time    : 2020/7/28 8:28 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : settings
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# 基本配置 其他环境的通用配置
class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 456
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('AmeBlog Admin', MAIL_USERNAME)

    AMEBLOG_MAIL = os.getenv('AMEBLOG_MAIL')
    AMEBLOG_POST_PER_PAGE = 10
    AMEBLOG_MANAGE_POST_PER_PAGE = 15
    AMEBLOG_COMMENT_PER_PAGE = 15


# 开发配置
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


# 测试配置
class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 内存数据库


# 生产配置
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# @Time    : 2020/7/28 8:27 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : fakes
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random

from .models import Admin, Category, Post, Comment
from .extensions import db


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='AmeBlog',
        blog_sub_title='雨过初晴的博客',
        name='Choyeon',
        about='联系邮件：admin@choyeon.cn'
    )
    # TODO:貌似没有添加密码
    db.session.add(admin)
    db.commit()


faker = Faker('zh_CN')


def fake_category(count=10):
    category = Category(name="Default")
    db.session.add(category)
    for i in range(count):
        category = Category(name=faker.word())
        db.session.add(category)
        try:
            db.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=faker.sentence(),
            body=faker.text(2000),
            category=Category.query.get(random.randint(1, Category.count())),
            timestamp=faker.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.count()))
        )
        db.session.add(comment)
    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.count()))
        )
        db.session.add(comment)
        comment = Comment(
            author='Choyeon',
            email='admin@choyeon.cm',
            site='https://choyeon.cn',
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.count()))
        )
        db.session.add(comment)
    db.session.commit()
    for i in range(salt):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=False,
            replied=Comment.query.get(random.randint(1, Comment.count())),
            post=Post.query.get(random.randint(1, Post.count()))
        )
        db.session.add(comment)
    db.session.commit()

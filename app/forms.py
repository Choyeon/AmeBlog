# @Time    : 2020/7/28 8:26 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError, TextAreaField, \
    HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional
from flask_ckeditor import CKEditorField

from app.models import Category


class BaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(BaseForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(4, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class PostForm(BaseForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', validators=[DataRequired()])
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = \
            [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


class CategoryForm(BaseForm):
    name = StringField('分类名', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('这个分类名已被使用')


class CommentForm(BaseForm):
    author = StringField('昵称', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('个人网站', validators=[DataRequired(), URL(), Length(0, 255)])
    body = TextAreaField('评论内容', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(BaseForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()


class SettingForm(BaseForm):
    name = StringField('设置名', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog标题', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog副标题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('关于页面内容', validators=[DataRequired()])
    submit = SubmitField()

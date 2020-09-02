# @Time    : 2020/7/28 8:26 下午
# @Author  : Choyeon
# @Email   : admin@choyeon.cn
# @Site    : https://www.choyeon.cn
# @File    : emails
from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from app.extensions import mail


async def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


async def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='文章收到评论', to=current_app.config['AMEBLOG_EMAIL'],
              html='<p>文章有新评论 <i>%s</i>,点击下面的链接进行检查:</p>'
                   '<p><a href="%s">%s</a></P>'
                   '<p><small style="color: #868e96">不要回复此电子邮件。</small></p>'
                   % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='评论收到恢复', to=comment.email,
              html='<p>对您发表的评论的新回复 <i>%s</i>, 点击下面的链接进行检查: </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">不要回复此电子邮件.</small></p>'
                   % (comment.post.title, post_url, post_url))

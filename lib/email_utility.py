from static.constants import SMTP_USER, SMTP_PASS

import dominate
from dominate.tags import *

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def form_email_contents(posts):
    doc = dominate.document(title="test")

    with doc.head:
        link(rel='stylesheet', href='../static/email_style.css')

    with doc:
        with table():
            with tr():
                th('아티클')
                th('리액션 수')
                th('댓글 수')
                th('공유 수')
                th('마지막 업데이트 시간')
                th('원게시물 링크')

            for post in posts:
                with tr():
                    th(post.message[:20])
                    th(post.numbers['reaction'])
                    th(post.numbers['comment'])
                    th(post.numbers['share'])
                    th(str(post.updated_time))
                    th(a('링크', href=post.link))

    return doc

def sendmail(to_addr, posts):
    message = MIMEMultipart('alternative')

    message['Subject'] = '<리포팅>TF-KR 지난 7일간의 Top 포스팅 목록'
    message['From'] = SMTP_USER
    message['To'] = to_addr

    contents = form_email_contents(posts)
    message.attach(MIMEText(str(contents), 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_addr, message.as_string())    
from typing import List

from static.constants import SMTP_USER, SMTP_PASS, FIRST_WORDS

import dominate
from dominate.tags import *

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_mailing_list() -> List[str]:
    with open('mailinglist.txt', 'r') as f:
        return f.readlines()

    return None

def form_email_contents(posts):
    doc = dominate.document(title="test")

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
                    message = f"{post.message[:FIRST_WORDS]} ....." if len(post.message) > FIRST_WORDS else post.message
                    th(message,                     style="text-align: left; padding-left: 10px; padding-right: 10px;")
                    th(post.numbers['reaction'],    style="text-align: center; padding-left: 10px; padding-right: 10px;")
                    th(post.numbers['comment'],     style="text-align: center; padding-left: 10px; padding-right: 10px;")
                    th(post.numbers['share'],       style="text-align: center; padding-left: 10px; padding-right: 10px;")
                    th(str(post.updated_time),      style="text-align: center; padding-left: 10px; padding-right: 10px;")
                    th(a('링크', href=post.link),    style="text-align: center; padding-left: 10px; padding-right: 10px;")

    return doc

def sendmail(posts):
    if (mailinglist := get_mailing_list()) is not None:
        mailinglist = get_mailing_list()

        message = MIMEMultipart('alternative')

        message['Subject'] = '<리포팅>TF-KR 지난 7일간의 Top 포스팅 목록'
        message['From'] = SMTP_USER
        message['To'] = ", ".join(mailinglist)

        contents = form_email_contents(posts)
        message.attach(MIMEText(str(contents), 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, mailinglist, message.as_string())    
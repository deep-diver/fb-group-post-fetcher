from typing import List

from static.constants import *

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from premailer import transform

def get_mailing_list() -> List[str]:
    with open('mailinglist.txt', 'r') as f:
        return f.readlines()

    return None

def form_email_contents(posts):
    loader = FileSystemLoader('static/templates')
    env = Environment(loader=loader)
    template = env.get_template('cerberus-responsive.html')

    output = template.render(head_logo=HEAD_LOGO,
                             head_image=HEAD_IMAGE,
                             head_section_article=HEAD_ARTICLE,
                             head_section_button_title=HEAD_BUTTON_TITLE,
                             bottom_section_article=BOTTOM_ARTICLE,
                             posts=posts)

    return transform(output)    
    
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
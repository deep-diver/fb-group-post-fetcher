from typing import List

from static.constants import SMTP_USER, SMTP_PASS
from static.constants import HEAD_IMAGE, HEAD_ARTICLE

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
    template = env.get_template('template.html')

    output = template.render(head_image=HEAD_IMAGE,
                             head_section_article=HEAD_ARTICLE,
                             posts=posts[:10],
                             secondary_posts=posts[11:20])

    return transform(output)    
    
def sendmail(posts, title, since, until):
    if (mailinglist := get_mailing_list()) is not None:
        mailinglist = get_mailing_list()

        message = MIMEMultipart('alternative')

        message['Subject'] = f"{title} [{since} ~ {until}]"
        message['From'] = SMTP_USER
        message['To'] = ", ".join(mailinglist)

        contents = form_email_contents(posts)
        message.attach(MIMEText(str(contents), 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, mailinglist, message.as_string())
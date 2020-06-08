from typing import List

from static.constants import SMTP_USER, SMTP_PASS

from bs4 import BeautifulSoup
import markdown2

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_mailing_list() -> List[str]:
    with open('mailinglist.txt', 'r') as f:
        return f.readlines()

    return None

def form_email_contents(posts):
    """
        html class names
        - post_title
        - post_article
        - post_link
        - post_numbers
        - post_date
    """

    with open('static/template.html') as f:
        soup        = BeautifulSoup(f, 'html.parser')

        titles      = soup.select(".post_title")
        articles    = soup.select(".post_article")
        links       = soup.select(".post_link")
        numbers     = soup.select(".post_numbers")
        dates       = soup.select(".post_date")

        assert len(titles) == len(articles) == len(links) == len(numbers) == len(dates)

        for index in range(len(titles)):
            # new_article_div = soup.new_tag('div')
            # new_article_div.string = BeautifulSoup(markdown2.markdown(posts[index].message), 'html.parser')
            inner_article = markdown2.markdown(posts[index].message)
            inner_article = inner_article.replace('<h3>', '<h6>').replace('</h3>', '</h6>')
            inner_article = inner_article.replace('<h2>', '<h5>').replace('</h2>', '</h5>')
            inner_article = inner_article.replace('<h1>', '<h4>').replace('</h1>', '</h4>')
            articles[index].insert(0, BeautifulSoup(inner_article, 'html.parser'))

            links[index]['href'] = posts[index].link
            
            dates[index].string = str(posts[index].updated_time)
            
            new_numbers_strong = soup.new_tag('strong')
            new_numbers_strong.string = f"리액션: {posts[index].numbers['reaction']}, 댓글: {posts[index].numbers['comment']}, 공유: {posts[index].numbers['share']}" 
            numbers[index].insert(0, new_numbers_strong)

        return str(soup)

    return None

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
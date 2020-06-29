import json
import datetime

from lib.model.facebook_post import FacebookPost
from typing import List
import markdown2 

from static.constants import FIRST_WORDS

def parsing_indivisual_post(data) -> FacebookPost:
    return FacebookPost.from_json(data)

def parsing(raw_text, since, until) -> List:
    parsed = json.loads(raw_text)
    tmp_posts = parsed["data"]

    posts = []
    count = 0

    for tmp_post in tmp_posts:
        since = datetime.datetime.strptime(since, "%Y-%m-%d").strftime("%Y-%m-%d")
        until = datetime.datetime.strptime(until, "%Y-%m-%d").strftime("%Y-%m-%d")
        created_time = FacebookPost.get_time(tmp_post, "Asia/Seoul")

        if since <= created_time <= until:
            if post := parsing_indivisual_post(tmp_post):
                posts.append(post)
                count = count+1

    return posts
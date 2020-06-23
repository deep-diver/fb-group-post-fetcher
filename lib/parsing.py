import json
import datetime

from lib.model.facebook_post import FacebookPost
from typing import List

def parsing_indivisual_post(data) -> FacebookPost:
    return FacebookPost.from_json(data)

def parsing(raw_text, since, until) -> List:
    parsed = json.loads(raw_text)
    tmp_posts = parsed["data"]

    posts = []

    for tmp_post in tmp_posts:
        since = datetime.datetime.strptime(since, "%Y-%m-%d").strftime("%Y-%m-%d")
        until = datetime.datetime.strptime(until, "%Y-%m-%d").strftime("%Y-%m-%d")
        created_time = datetime.datetime.strptime(tmp_post.get("created_time"), "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")

        if since <= created_time <= until:
            if post := parsing_indivisual_post(tmp_post):
                posts.append(post)

    return posts
import json
from lib.model.facebook_post import FacebookPost
from typing import List

def parsing_indivisual_post(data) -> FacebookPost:
    return FacebookPost.from_json(data)

def parsing(raw_text) -> List:
    print(raw_text)
    parsed = json.loads(raw_text)
    tmp_posts = parsed["data"]

    posts = []

    for tmp_post in tmp_posts:
        if post := parsing_indivisual_post(tmp_post):
            posts.append(post)

    return posts
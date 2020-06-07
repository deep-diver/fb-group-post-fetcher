import json
from lib.model.facebook_post import FacebookPost
from typing import List

def parsing_indivisual_post(data) -> FacebookPost:
    return FacebookPost.from_json(data)

def parsing(raw_text) -> List:
    parsed = json.loads(raw_text)
    tmp_posts = parsed["data"]

    posts = []

    for tmp_post in tmp_posts:
        post = parsing_indivisual_post(tmp_post)
        print(post)
        posts.append(post)

    return posts
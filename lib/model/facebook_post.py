from __future__ import annotations

import datetime
from typing import Dict

class FacebookPost(object):
    """
    글(Post)를 나타냅니다.
    """

    id          : str
    message     : str
    numbers     : Dict[str, int] # reactions, comments, shares
    link        : str
    updated_time: datetime.datetime

    @classmethod
    def from_json(cls, message_json: dict) -> FacebookPost:
        print(message_json)
        post = FacebookPost()

        post.id             = message_json.get("id")
        post.message        = message_json.get("message", "")
        post.link           = message_json.get("permalink_url")
        
        post.updated_time   = datetime.datetime.strptime(
            message_json.get("updated_time"), "%Y-%m-%dT%H:%M:%S%z"
        )

        post.numbers = {}
        post.numbers["reaction"]    = message_json.get("reactions").get("summary").get("total_count")
        post.numbers["share"]       = message_json.get("shares").get("count") if "shares" in message_json else 0
        post.numbers["comment"]     = message_json.get("comments").get("summary").get("total_count")
        return post

    def __repr__(self) -> str:
        return f"FB_POST(id={self.id}, message={self.message}, link={self.link}, updated_time={self.updated_time}, numbers={self.numbers})"

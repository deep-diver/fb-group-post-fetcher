from __future__ import annotations

import datetime
import markdown2 
from typing import Dict, List

from static.constants import FIRST_WORDS

class FacebookPost(object):
    """
    글(Post)를 나타냅니다.
    """

    id          : str
    message     : str
    numbers     : Dict[str, int] # reaction, comment, share
    link        : str
    attachments : List[str]
    front_image : str
    updated_time: datetime.datetime

    @classmethod
    def from_json(cls, message_json: dict) -> FacebookPost:
        print(message_json)
        post = FacebookPost()

        post.id             = message_json.get("id")
        post.link           = message_json.get("permalink_url")
        
        post.message        = message_json.get("message", "")
        if post.message == "": post.message = "내용이 비어있는 게시글 입니다 (공유/이미지만을 포함할 수 있습니다)"
        tmp_message         = markdown2.markdown(post.message[:FIRST_WORDS])
        post.message        = f"{tmp_message}..." if len(post.message) > len(tmp_message) else tmp_message

        post.updated_time   = datetime.datetime.strptime(
            message_json.get("updated_time"), "%Y-%m-%dT%H:%M:%S%z"
        ).strftime("%Y-%m-%d, %H:%M")

        post.numbers = {}
        post.numbers["reaction"]    = message_json.get("reactions").get("summary").get("total_count")
        post.numbers["share"]       = message_json.get("shares").get("count") if "shares" in message_json else 0
        post.numbers["comment"]     = message_json.get("comments").get("summary").get("total_count")

        post.attachments = []
        if attachments := message_json.get("attachments"):
            for attachment in attachments.get("data"):
                if image := attachment.get("media").get("image"):
                    post.attachments.append(image.get("src"))

        post.front_image = post.attachments[0] if len(post.attachments) > 0 else "https://dummyimage.com/270x270/c4c4c4/fff.png&text=no+image"

        return post

    def __repr__(self) -> str:
        return f"FB_POST(id={self.id}, message={self.message}, link={self.link}, updated_time={self.updated_time}, numbers={self.numbers})"

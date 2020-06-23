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

    def __replace_h_size(self, message) -> str:
        return message.replace("h3", "h5") \
                      .replace("h2", "h4") \
                      .replace("h1", "h3")

    def __set_message(self, message_json) -> str:
        result = message_json.get("message", "")
        
        if result.strip() == "":
            print(message_json)
            if attachments := message_json.get("attachments"):
                for attachment in attachments.get("data"):
                    description = attachment.get("description", "")
                    if description != "": 
                        result = description
                        break
        
        if result == "":
            return None

        result = f"{result[:FIRST_WORDS]} ..... " if len(result) > FIRST_WORDS else result
        result = markdown2.markdown(result)
        result = self.__replace_h_size(result)

        return result

    @classmethod
    def from_json(cls, message_json: dict) -> FacebookPost:
        post = FacebookPost()

        post.updated_time   = datetime.datetime.strptime(
            message_json.get("created_time"), "%Y-%m-%dT%H:%M:%S%z"
        ).strftime("%Y-%m-%d, %H:%M")

        if message := post.__set_message(message_json):
            post.message = message
        else:
            return None 

        post.id             = message_json.get("id")
        post.link           = message_json.get("permalink_url")

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

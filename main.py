import os
import asyncio
import aiohttp
import argparse

from static.constants import BASE_URL, TAIL_URL
from static.constants import FIRST_WORDS, SUB_FIRST_WORDS, TOP_K
from lib.token_refresh import *
from lib.parsing import *
from lib.email_utility import *

def handle_post_message_length(posts):
    for idx, post in enumerate(posts):
        if idx < 10:
            post.message = f"{post.message[:FIRST_WORDS]} ..... " if len(post.message) > FIRST_WORDS else post.message
            post.message = markdown2.markdown(post.message)
            post.message = FacebookPost.replace_h_size(post.message)
        else:
            post.message = post.message.replace("**", "").strip()
            post.message = f"{post.message[:SUB_FIRST_WORDS]} ..." if len(post.message) > SUB_FIRST_WORDS else post.message

async def fetch_posts(URL, WEIGHTS_REACTIONS, WEIGHTS_SHARES, WEIGHTS_COMMENTS, EMAIL_TITLE, SINCE, UNTIL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            posts = parsing(await res.text(), SINCE, UNTIL)
            sortedPost = sorted(posts, key=lambda post: 
                                            (post.numbers["reaction"]    * WEIGHTS_REACTIONS + 
                                             post.numbers["share"]       * WEIGHTS_SHARES + 
                                             post.numbers["comment"]     * WEIGHTS_COMMENTS), reverse=True)
            handle_post_message_length(sortedPost)
            sendmail(sortedPost[:TOP_K], EMAIL_TITLE, SINCE, UNTIL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please specify the range of dates and the number of posts to be collected')
    parser.add_argument('--since', required=True, type=str, help='dates in YYYY-MM-DD') 
    parser.add_argument('--until', required=True, type=str, help='dates in YYYY-MM-DD')
    parser.add_argument('--email-title', required=True, type=str, help='title for the email')
    parser.add_argument('--limit', required=False, type=int, default=300, help='number of posts to scrap')
    parser.add_argument('--weight-reactions', required=False, type=float, default=1.0, help='from 0 to 1')
    parser.add_argument('--weight-shares', required=False, type=float, default=1.0, help='from 0 to 1')
    parser.add_argument('--weight-comments', required=False, type=float, default=1.0, help='from 0 to 1')
    args = parser.parse_args()

    access_token = update_token()
    load_dotenv()

    URL = f"{BASE_URL}&limit={args.limit}&since={args.since}&until={args.until}&{TAIL_URL}&access_token={access_token}"

    asyncio.run(fetch_posts(URL, 
                            args.weight_reactions, 
                            args.weight_shares, 
                            args.weight_comments,
                            args.email_title,
                            args.since,
                            args.until))


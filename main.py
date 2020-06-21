import os
import asyncio
import aiohttp
import argparse

from static.constants import *
from lib.token_refresh import *
from lib.parsing import *
from lib.email_utility import *

# def mock_html(posts):
#     loader = FileSystemLoader('static/templates')
#     env = Environment(loader=loader)
#     template = env.get_template('cerberus-responsive.html')

#     output = template.render(head_logo=HEAD_LOGO,
#                              head_image=HEAD_IMAGE,
#                              head_section_article=HEAD_ARTICLE,
#                              head_section_button_title=HEAD_BUTTON_TITLE,
#                              posts=posts)

#     with open('output.html', 'w') as f:
#         f.write(output)

async def fetch_posts(URL, WEIGHTS_REACTIONS, WEIGHTS_SHARES, WEIGHTS_COMMENTS):
    # 비동기 http 클라이언트 세션 생성
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            posts = parsing(await res.text())
            sortedPost = sorted(posts, key=lambda post: 
                                            post.numbers["reaction"]    * WEIGHTS_REACTIONS + 
                                            post.numbers["share"]       * WEIGHTS_SHARES + 
                                            post.numbers["comment"]     * WEIGHTS_COMMENTS, reverse=True)
            # mock_html(sortedPost[:TOP_K])
            sendmail(sortedPost[:TOP_K])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please specify the range of dates and the number of posts to be collected')
    parser.add_argument('--since', required=True, type=str, help='dates in YYYY-MM-DD') 
    parser.add_argument('--until', required=True, type=str, help='dates in YYYY-MM-DD') 
    parser.add_argument('--limit', required=False, type=int, default=100, help='number of posts to scrap')
    parser.add_argument('--weight-reactions', required=False, type=float, default=1.0, help='from 0 to 1')
    parser.add_argument('--weight-shares', required=False, type=float, default=1.0, help='from 0 to 1')
    parser.add_argument('--weight-comments', required=False, type=float, default=1.0, help='from 0 to 1')
    args = parser.parse_args()

    access_token = update_token()
    load_dotenv()

    URL = f"{BASE_URL}&limit={args.limit}&since={args.since}&until={args.until}&{TAIL_URL}&access_token={access_token}"
    asyncio.run(fetch_posts(URL, args.weight_reactions, args.weight_shares, args.weight_comments))


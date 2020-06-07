import asyncio
import aiohttp
import argparse

from static.constants import *
from lib.parsing import *

async def fetch_posts(URL):
    # 비동기 http 클라이언트 세션 생성
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            posts = parsing(await res.text())
            sortedPost = sorted(posts, key=lambda post: 
                                            post.numbers["reaction"]    * WEIGHTS_REACTIONS + 
                                            post.numbers["share"]       * WEIGHTS_SHARES + 
                                            post.numbers["comment"]     * WEIGHTS_COMMENTS, reverse=True)
            print(sortedPost)

if __name__ == "__main__":
    # 시작, 끝 날짜 사용자 입력
    parser = argparse.ArgumentParser(description='dates input')
    parser.add_argument('since', type=str, help='dates in YYYY-MM-DD') 
    parser.add_argument('until', type=str, help='dates in YYYY-MM-DD') 
    parser.add_argument('limit', type=int, help='number of posts to scrap')
    args = parser.parse_args()

    URL = f"{BASE_URL}&limit={args.limit}&since={args.since}&until={args.until}&{TAIL_URL}"
    asyncio.run(fetch_posts(URL))


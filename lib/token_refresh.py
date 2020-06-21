import os
import asyncio
from dotenv import load_dotenv, set_key

from typing import NamedTuple
import datetime

import aiohttp

class Token(NamedTuple):
    access_token: str
    token_type: str
    expires_in: datetime.datetime

def update_token():
    load_dotenv()

    APP_ID          = os.getenv("APP_ID")
    APP_SECRET      = os.getenv("APP_SECRET")    
    ACCESS_TOKEN    = os.getenv("FB_ACCESS_TOKEN")

    token = asyncio.run(refresh_token(APP_ID, APP_SECRET, ACCESS_TOKEN))
    set_key(".env", "FB_ACCESS_TOKEN", token.access_token)

    return token.access_token

async def refresh_token(app_id: str, app_secret: str, access_token: str) -> Token:
    """Exchanges access_token with a long term access token (expires in 60+ days)"""
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": access_token,
    }

    base_url = "https://graph.facebook.com/v7.0/oauth/access_token"

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as resp:
            data = await resp.json()
            print(data)

            now = datetime.datetime.now()
            expires_in = now + datetime.timedelta(seconds=data["expires_in"])

            return Token(
                access_token=data["access_token"],
                token_type=data["token_type"],
                expires_in=expires_in,
            )
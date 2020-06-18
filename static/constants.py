import os
from dotenv import load_dotenv

load_dotenv()

GROUP_ID        = os.getenv("FB_GROUP_ID")
ACCESS_TOKEN    = os.getenv("FB_ACCESS_TOKEN")
SMTP_USER       = os.getenv("SMTP_USER")
SMTP_PASS       = os.getenv("SMTP_PASS")

BASE_URL = f"https://graph.facebook.com/v7.0/{GROUP_ID}/feed?"
TAIL_URL = f"fields=message%2Creactions.summary(total_count)%2Ccomments.summary(total_count)%2Cpermalink_url%2Cshares%2Cupdated_time%2Cattachments{{media}}&access_token={ACCESS_TOKEN}"

TOP_K       = int(os.getenv("TOP_K"))
FIRST_WORDS = int(os.getenv("FIRST_WORDS"))
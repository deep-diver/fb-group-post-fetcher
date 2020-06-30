import os
from dotenv import load_dotenv
from configparser import ConfigParser

load_dotenv()
cfgParser = ConfigParser()
cfgParser.read('config.cfg')

GROUP_ID    = cfgParser.get('fb', 'FB_GROUP_ID')
BASE_URL    = f"https://graph.facebook.com/v7.0/{GROUP_ID}/feed?"
TAIL_URL    = f"fields=message%2Creactions.summary(total_count)%2Ccomments.summary(total_count)%2Cpermalink_url%2Cshares%2Cupdated_time%2Cattachments{{media}}%2Ccreated_time"
SMTP_USER   = os.getenv("SMTP_USER")
SMTP_PASS   = os.getenv("SMTP_PASS")

TOP_K           = int(cfgParser.get('config', 'TOP_K'))
FIRST_WORDS     = int(cfgParser.get('config', 'FIRST_WORDS'))
SUB_FIRST_WORDS = int(cfgParser.get('config', 'SUB_FIRST_WORDS'))
HEAD_IMAGE      = cfgParser.get('web', 'HEAD_IMAGE')
HEAD_ARTICLE    = cfgParser.get('web', 'HEAD_ARTICLE')
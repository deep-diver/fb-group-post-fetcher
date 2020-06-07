# Facebook Group Post Fetcher + Emailing

This repository contains simple source codes to scrap posts from a certain facebook group. The following information is included.

- id
- message
- link
- updated time
- number of reactions
- number of comments
- number of shares

Also the scrapped posts are sorted via the following formula. You can change the weights from the CLI. Please look at the section below.

## Usage

### CLI
```shell
$ python main.py --help
usage: main.py [-h] --since SINCE --until UNTIL [--limit LIMIT] [--weight-reactions WEIGHT_REACTIONS]
               [--weight-shares WEIGHT_SHARES] [--weight-comments WEIGHT_COMMENTS]

Please specify the range of dates and the number of posts to be collected

optional arguments:
  -h, --help            show this help message and exit
  --since SINCE         dates in YYYY-MM-DD
  --until UNTIL         dates in YYYY-MM-DD
  --limit LIMIT         number of posts to scrap
  --weight-reactions WEIGHT_REACTIONS
                        from 0 to 1
  --weight-shares WEIGHT_SHARES
                        from 0 to 1
  --weight-comments WEIGHT_COMMENTS
                        from 0 to 1
```

### Example
```shell
$ python main.py --from 2020-01-10 --until 2020-01-20
```

```shell
$ python main.py --from 2020-01-10 --until 2020-01-20 --limit 50
```

```shell
$ python main.py --from 2020-01-10 --until 2020-01-20 --limit weights-reactions=0.5 --weights-shares=0.8 --weights-comments=1
```

## Requirements

You must specify the following two values via `.env`. `.env` is something you need to create on your own.

### Facebook Specific Information

In order to enable facebook specific information, you may need to follow the [instructions](https://developers.facebook.com/docs/groups-api/). However, you dont' need to request `App Review` process if you just want to test not deploying to the real world. 

```
FB_GROUP_ID=XXX

# You can generate a temporary access token for testing purpose
# via https://developers.facebook.com/tools/explorer/
FB_ACCESS_TOKEN=XXX
```

### SMTP Specific Information
```
# USER is the same as your email address
SMTP_USER=XXX

# This password is **not** your email's password. 
# For example, this is your emails app password in Gmail.
SMTP_PASS=XXX
```
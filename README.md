![newsletter_every_fri](https://github.com/deep-diver/fb-group-post-fetcher/workflows/newsletter_every_fri/badge.svg?branch=master)
![newsletter_every_wed_sun](https://github.com/deep-diver/fb-group-post-fetcher/workflows/newsletter_every_wed_sun/badge.svg?branch=master)
![newletter_every_14th_day](https://github.com/deep-diver/fb-group-post-fetcher/workflows/newletter_every_14th_day/badge.svg?branch=master)


# Facebook Group Post Fetcher + Emailing

<img src="https://github.com/deep-diver/fb-group-post-fetcher/blob/master/static/images/process.png?raw=true" width="550px"/>

This repository contains simple source codes to scrap posts from a certain facebook group. The following information is included.

- id
- message
- link
- created time
- number of reactions
- number of comments
- number of shares

Also the scrapped posts are sorted via the following formula. You can change the weights from the CLI. Please look at the section below.
```
  (# of reactions * WEIGHT_REACTIONS) + (# of shares * WEIGHT_SHARES) + (# of comments * WEIGHT_COMMENTS)
```

## Look

<img src="https://github.com/deep-diver/fb-group-post-fetcher/blob/master/static/images/preview.png?raw=true" height="800px"/>

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
$ python main.py --since 2020-01-10 --until 2020-01-20
```

```shell
$ python main.py --since 2020-01-10 --until 2020-01-20 --limit 50
```

```shell
$ python main.py --since 2020-01-10 --until 2020-01-20 --limit weights-reactions=0.5 --weights-shares=0.8 --weights-comments=1
```

## Requirements (Mantatory)

You must specify the following four values via `.env`. `.env` is something you need to create on your own.

### Facebook Specific Information

In order to enable facebook specific information, you may need to follow the [instructions](https://developers.facebook.com/docs/groups-api/). However, you dont' need to request `App Review` process if you just want to test not deploying to the real world. In this case, you could just get a temporary access token via [Graph API Explorer](https://developers.facebook.com/tools/explorer/)

```
FB_GROUP_ID=XXX

# You can generate a temporary access token for testing purpose
# via https://developers.facebook.com/tools/explorer/
FB_ACCESS_TOKEN=XXX
```

Initial token is issued for temporary purpose. If you want to have long lived access token, you need to exchange the temporary token with it. You can do that via accessing an [API](https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing/). This API requires your APP ID and APP Secret, so you should write these information into the `.env` file.

```
APP_ID=XXX
APP_SECRET=XXX
```

For the first time you run the application, you will need a temporary access token. After that, whenever you run the application again, the current access token will be refreshed with a new long lived one. Make sure you encrypt the `.env` so only you can access the `APP_ID` and `APP_SECRET`.

### SMTP Specific Information
```
# USER is the same as your email address
SMTP_USER=XXX

# This password is **not** your email's password. 
# For example, this is your emails app password in Gmail.
SMTP_PASS=XXX
```

Along with these, you also need to specify the list of email addresses which you want to send an email to. You can edit the list in `mailinglist.txt`. Just put an email address with a line break.

## Requirements (Optional)

You could modify some variables in `.env` file to meet your need

### TOP_K
This one specify the number of Top K posts to keep as in the email content.

### FIRST_WORDS
Message for a post could be too long. This variable specify the number of words to keep to be appeared as in the email content.


### `.env` example
```
APP_ID=XXX
APP_SECRET=XXX

FB_GROUP_ID=XXX
FB_ACCESS_TOKEN=XXX

SMTP_USER=XXX
SMTP_PASS=XXX

TOP_K=10
FIRST_WORDS=50
```

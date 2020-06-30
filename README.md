![newsletter_every_fri](https://github.com/deep-diver/fb-group-post-fetcher/workflows/newsletter_every_fri/badge.svg?branch=master)

# Facebook Group Post Fetcher + Emailing

<img src="https://github.com/deep-diver/fb-group-post-fetcher/blob/master/static/images/process.png?raw=true" width="550px"/>

This repository is about scrapping a Facebook's group posts and sending out a email newsletter.
- you must be an admin of the target facebook group
- you must create a facebook app with a Group Post permission (app doesn't have be reviewed though)
  - please follow this page for [Groups API](https://developers.facebook.com/docs/groups-api/)
- email receivers could be configured via `mailinglist.txt`

## How it works
It works with GitHub action, but you can run locally as well.

1. GitHub Action dycryptes `.env.gpg`, and you will get `.env`
2. GitHub Action triggers this application running
  - exchange facebook's `access token` with a long-lived one
  - replace the exchanged token to the existing one in `.env`
  - grab group posts via Facebook's Graph API
  - sort them
  - inject posts's information into HTML (jinja)
  - HTML/CSS will be nicely formatted for email (premailer)
  - email will be sent to those listed in `mailinglist.txt`
3. GitHub Action deletes `.env.gpg`
4. GitHub Action encrypts `.env` into `.env.gpg`
5. GitHub Action pushes `.env.gpg` to your current repository

## Look

<img src="https://github.com/deep-diver/fb-group-post-fetcher/blob/master/static/images/preview.png?raw=true" height="800px"/>

## Usage

### CLI
```shell
$ python main.py --help
usage: main.py [-h] --since SINCE --until UNTIL --email-title EMAIL_TITLE [--limit LIMIT] 
               [--weight-reactions WEIGHT_REACTIONS] [--weight-shares WEIGHT_SHARES] [--weight-comments WEIGHT_COMMENTS]

Please specify the range of dates and the number of posts to be collected

optional arguments:
  -h, --help            show this help message and exit
  --since SINCE         dates in YYYY-MM-DD
  --until UNTIL         dates in YYYY-MM-DD
  --email-title EMAIL_TITLE
                        title for the email
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
$ python main.py --since 2020-01-10 \ 
                 --until 2020-01-20 \
                 --email-title="Weekly Newsletter"
```

```shell
$ python main.py --since 2020-01-10 \
                 --until 2020-01-20 \
                 --email-title="Weekly Newsletter" \
                 --limit 50
```

```shell
$ python main.py --since 2020-01-10 \
                 --until 2020-01-20 \
                 --email-title="Weekly Newsletter" \
                 --limit weights-reactions=0.5 \
                 --weights-shares=0.8 \
                 --weights-comments=1
```

## Config files

There are two config files. 
- .env
  - this dotenv file contains sensitive information
- config.cfg
  - this contains information that you can customize yourself
  
### .env

You should set values described below on your own.
- APP_ID: your facebook app id
- APP_SECRET: your facebook secret
- FB_ACCESS_TOKEN: access token issued via [Graph API Explorer](https://developers.facebook.com/tools/explorer/). make sure your access token belongs to your app.

```shell
APP_ID=XXX
APP_SECRET=XXX
FB_ACCESS_TOKEN=XXX

SMTP_USER=XXX
SMTP_PASS=XXX
```

`.env` only needs to be set initially. After you set `.env`, you have to encrypt it into `.env.gpg` using the command below. You must set your own password in `--passphrase` option. 

```shell
gpg2 --quiet --batch --yes --decrypt --passphrase="SYMMETRIC_KEY" --output=.env .env.gpg
```

Also you must set the same `passphrase` in the SECRETS for your GitHub Repo. Here is the steps for doing so.
1. Go to `Settings` tab.
2. Go to `SECRETS` menu on the left.
3. Click `New secret` button on the top left.
4. Set `Name` as `GPG_KEY`.
5. Set the value of the `GPG_KEY` to your choice as in `--passphrase`
6. Click `Add secret` button.


### config.cfg

The name of each key explains what they are. `TOP_K` means how many posts you want to grap. Only the TOP 10 posts will be included in the email with image. The rest will be included with only text. `FIRST_WORDS` means how many words you want to keep for the TOP 10 posts. `SUB_FIRST_WORDS` means how many words you want to keep for the other posts than TOP 10.

```shell
# config.cfg

[config]
TOP_K = XXX
FIRST_WORDS = XXX
SUB_FIRST_WORDS = XXX 

[fb]
FB_GROUP_ID = XXX

[web]
HEAD_IMAGE = image_url_to_appear_at_the_top_of_email
HEAD_ARTICLE = a_sentence_to_appear_at_the_top_of_email
```

Also the scrapped posts are sorted via the following formula. You can change the weights from the CLI. Please look at the Usage section.
```
  (# of reactions * WEIGHT_REACTIONS) + (# of shares * WEIGHT_SHARES) + (# of comments * WEIGHT_COMMENTS)
```

#!/usr/bin/python
#Twitter API object container
import ConfigParser
import tweepy

config = ConfigParser.ConfigParser()
config.read("oauth.conf")
CONSUMER_KEY    = config.get('Api', 'ApiKey')
CONSUMER_SECRET = config.get('Api', 'ApiSecret')
ACCESS_KEY      = config.get('Access', 'AccessToken')
ACCESS_SECRET   = config.get('Access', 'AccessSecret')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
global twitter
twitter = tweepy.API(auth)

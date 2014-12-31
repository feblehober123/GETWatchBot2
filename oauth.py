#!/usr/bin/python
#This is a script I copied from http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth/
#It's used to easily get the bot (or any app) authorized on a twitter account

import tweepy
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("oauth.conf")
CONSUMER_KEY    = config.get('Api', 'ApiKey')
CONSUMER_SECRET = config.get('Api', 'ApiSecret')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret

import requests
from requests.exceptions import *
import tweepy.error
from twitter import twitter
import json
from time import sleep
from datetime import datetime, timedelta
import repdigits
from config import HOURS_HUMAN_TWEET_IS_RELEVANT, NON_DUBS_BOARDS
import locale
# An explanation about the GET class:
# The GET class contains information about a board; its current post id,
# an older post id for reference, the next GET that will occur on the board,
# the posting rate, the time until the next GET will occur,
# and if the GET has been tweeted about yet.
# This time (as opposed to the original bot) there is only one function,
# update(), which updates all the member variables. I may choose to add
# the "push" time estimation algorithm late but for now update() will only
# use the "total" algorithm.
# I have tried and partially failed at making this class reusable by
# other things; I suggest you read it through before using.

s = requests.Session()
s.headers.update({"User-Agent": "GETWatchBot/2.0 (@https://github.com/feblehober123/GETWatchBot2)"})

locale.setlocale(locale.LC_TIME, 'en_US') # <-- non-US-figs replace en_US 
# with a locale that has shortened month/weekday names compliant with 
# the HTTP Date RFC 1123 

class GET:
    def __init__(self, board):
        self.board = board
        self.new_post       = 0 #will be a json post dict
        self.old_post       = 0 #will also be a json post dict
        self.next_GET       = 0
        self.tweeted        = False
        self.posting_rate   = 0.0 #measured in posts/minute
        self.time_GET_occurs= datetime(year=1900, month=1, day=1)
        self.time_updated   = datetime(year=1900, month=1, day=1)
        self.update()
    def __repr__(self):
        return "<{post_num} GET on /{board}/>".format(post_num=self.next_GET, board=self.board)
    def update(self):
        #retries 5 times until success, and sleeps 15 minutes on error
        
        #get threads.json, store datetime.utcnow() into time_updated
        #compare last_updated and find oldest/newest, store
        #use C function next_GET to determine next_GET
        #use tweepy to search for tweets about GET
        #measure posting_rate
        #determine time GET occurs

        for i in range(0,5):
            try:
                r = s.get('http://a.4cdn.org/'+self.board+'/threads.json',
                    headers={'If-Modified-Since':self.time_updated.strftime('%a, %d %b %Y %H:%M:%S GMT')})
                if (r.status_code == 304):   #304 is not modified for you HTTP plebs
                    #skip next part or return
                    self.time_updated = datetime.utcnow()
                    return
                r.raise_for_status()
                jthrs = json.loads(r.content)
                newest_thr = jthrs[-1]['threads'][-1]   #set newest to oldest
                oldest_thr = jthrs[0]['threads'][0]     #and oldest to newest
                for page in jthrs:  #then find the actual newest/oldest
                    for thr in page['threads']:
                        if (thr['last_modified'] > newest_thr['last_modified'] and datetime.utcfromtimestamp(thr['last_modified']) < datetime.utcnow()):
                            newest_thr = thr
                        if (thr['last_modified'] < oldest_thr['last_modified']):
                            oldest_thr = thr
                r = s.get('http://a.4cdn.org/'+self.board+'/thread/'+str(newest_thr['no'])+'.json')
                r.raise_for_status()
                newest_thr = json.loads(r.content)
                self.new_post = newest_thr['posts'][-1]
                for i in range(0,5):
                    try:
                        sleep(1.0)    #one request per second
                        r = s.get('http://a.4cdn.org/'+self.board+'/thread/'+str(oldest_thr['no'])+'.json')
                        r.raise_for_status()
                    except HTTPError as e:
                        print i
                        if (r.status_code == 404):
                            if (i == 4):
                                raise
                            oldest_thrs = sorted(jthrs[-1]['threads'], key = lambda x: x['last_modified'], reverse=False)
                            oldest_thr = oldest_thrs[4-i] #hope the rest haven't 404'd either
                            continue
                        else:
                            raise
                    break
                        
                oldest_thr = json.loads(r.content)
                self.old_post = oldest_thr['posts'][-1]
                
                if (self.board in NON_DUBS_BOARDS):
                    self.next_GET = int(str(int(str(self.new_post['no'])[:-6])+1) + '0'*6)   #not creating a C function for clear GETs right now
                else:
                    self.next_GET = repdigits.nextget(self.new_post['no'], 6)
                
		self.tweeted = False
                timeline = twitter.user_timeline(count=20)
                for status in timeline:
                    if '/'+self.board+'/' in status.text:   #Do not tweet if a human has mentioned the board in the past hour
                        if (datetime.utcnow() - status.created_at).total_seconds()/3600.0 < HOURS_HUMAN_TWEET_IS_RELEVANT:
                            self.tweeted = True
                            break
                
                if (((self.new_post['time'] - self.old_post['time'])/60.0) > 0):
                    self.posting_rate = (self.new_post['no'] - self.old_post['no'])/((self.new_post['time'] - self.old_post['time'])/60.0)
                else:
                    self.posting_rate = 0.0
                
                if (self.posting_rate != 0):
                    self.time_GET_occurs = datetime.utcfromtimestamp(self.new_post['time']) + timedelta(minutes=(self.next_GET - self.new_post['no'])/self.posting_rate)
                else:
                    self.time_GET_occurs = datetime.utcfromtimestamp(self.new_post['time']) + timedelta(days=10)
                
                self.time_updated = datetime.utcnow()
            except (RequestException, ConnectionError, HTTPError, Timeout) as e:
                if ('404' in e.message):
                    print 'ERROR: Internet error: 404.', "Sleeping 2 minutes..."
                    sleep(2*60)
                    if (i == 4):
                        raise
                    continue
                print "ERROR: Internet error: ", e.message, ".", "Sleeping 15 minutes..."
                sleep(15*60)
                if (i == 4):
                    raise
                continue
            except tweepy.error.TweepError as TError:
                if ('Rate limit exceeded' in TError[0][0]['message']):
                    print "Twitter rate limit exceeded when updating. Sleeping 15 minutes..."
                else:
                    print "Error: Tweepy: ", TError[0][0]['message'], "Sleeping 15 minutes..."
                sleep(15*60)
                if (i == 4):
                    raise
                continue
            except ValueError as e:
                if ('json' in e.message.lower()):
                    print "Error: Invalid JSON recieved from 4chan. Sleeping 15 minutes..."
                    sleep(15*60)
                    if (i == 4):
                        raise
                    continue
                else:
                    raise
            break

#!/usr/bin/python
from GET import GET
from time import sleep
import time
from datetime import timedelta, datetime
from sys import stdout, stdin
import requests
from requests.exceptions import *
import json
from twitter import twitter
import repdigits
import locale

### CONFIG
from config import *

GET_TEXT = "{get_name} coming up on /{board}/ in about {time_until} minutes (~{posts_to_go} posts)."
NEW_BOARD_TEXT = "New board: /{board}/ \nGet all the early GETs!"

### DEFINITIONS BEFORE MAIN LOOP
#detect new boards and tweet about them
def update_boards(boards):    #update list of boardnames, and tweet about new ones
    try:
        r = s.get('http://a.4cdn.org/boards.json')  #don't bother with If-Modified-Since
        r.raise_for_status()
        jbrds = json.loads(r.content)
        new_listed_boards = []
        for json_board in r.json()['boards']:
            new_listed_boards.append(json_board)
    except (RequestException, ConnectionError, HTTPError, Timeout) as e:
        print "Error getting boards from 4chan. Using old boards instead."
        return boards
    new_boards = [new_listed_board['board']    for new_listed_board in new_listed_boards]
    if boards != new_boards:    #If there is a new board...
        try:
            with open('.boards_cache.txt', 'r') as f:
                last_update_timestamp = f.readline()    #Get last time boards were updated
        except IOError:
            open('.boards_cache.txt', 'w').close()  #Create file if it doesn't exist
            last_update_timestamp = 0 
        if (time.time() - float(last_update_timestamp)) / 86400 < DAYS_NEW_BOARD_IS_FRESH:    #If the boards were updated recently enough...
            for new_board in new_boards:
                if not new_board in boards:
                    print "New board: "+new_board
                    #print NEW_BOARD_TEXT.format(board=new_board)
                    twitter.update_status(NEW_BOARD_TEXT.format(board=new_board))
        boards = new_boards    #Update boards
    with open('.boards_cache.txt', 'w') as f:
        f.write(str(time.time())+'\n')
        for listed_board in boards:
            f.write(listed_board+'\n')
    return boards

#Returns the name of a GET
def GET_name(GET):
    if str(GET)[-1] == 9:   #Change 9s to 0s, e.g. 1999999 becomes 2000000
        GET += 1
    GETs = str(GET)
    if GETs[-6] == GETs[-1] == 0:   #Change clear GETs to the M value, e.g. 2000000 becomes 2M GET instead of just sexts
        return GETs[:-6]+"M GET"
    GETValue = repdigits.repdigits(GET)
    GET_names_dict = {
        5: 'quints',    #this one should never be printed
        6: 'sexts',
        7: 'septs',
        8: 'octs',
        9: 'nons',
        10: 'Fuggin huge GET'
    }
    return GET_names_dict[GETValue]



### STARTUP CODE BEFORE MAIN LOOP

locale.setlocale(locale.LC_TIME, 'en_US') # <-- non-US-figs replace en_US 
# with a locale that has shortened month/weekday names compliant with 
# the HTTP Date RFC 1123 

try:
    f = open('.boards_cache.txt', 'r')
    f.read().split()[0]
    f.close()
except (IOError, IndexError):
    f = open('.boards_cache.txt', 'w')
    f.write('0')
    f.close()  #creates the file if it doesnt exist

with open('.boards_cache.txt', 'ra') as f:    #load cached boardnames, so I can$
    l = f.read().split()
    timestamp = l[0]    #first line is the time boardnames were saved
    boardnames = l[1:]  #the rest are the boards

s = requests.Session()
s.headers.update({"User-Agent": "GETWatchBot/2.0 (@https://github.com/feblehober123/GETWatchBot2)"})

print "Updating boardnames..."
boardnames = update_boards(boardnames)

#Initialize list of GET classes
stdout.write('Initializing boards... ')
stdout.flush()
boards = []
for boardname in boardnames:
    stdout.write(boardname+' ')
    stdout.flush()
    boards.append(GET(boardname))
stdout.write('done!\n')
stdout.flush()



### MAIN LOOP
while True:
    print 'Starting loop!'
    print 'Updating boardnames...'
    boardnames = update_boards(boardnames)
    for board in boards:
        board.update()
        next_GET = repdigits.nextget(board.new_post['no'], 6)
        #if (board.next_GET != next_GET):  #check if the GET is over
            #board.next_GET = next_GET  #why did i put this in? =[
        posts_to_go = board.next_GET - board.new_post['no']
        posts_to_go = round(posts_to_go, 1-len(str(posts_to_go)))   #round to the first digit
        min_until = (board.time_GET_occurs - datetime.utcnow()).total_seconds()/60.0
        print "Time until /"+board.board+'/ '+GET_name(board.next_GET)+": ", str(timedelta(minutes=round(min_until)))
        if (min_until < MINUTES_GET_IS_SOON and min_until > MINUTES_GET_IS_UPON_US):
            if board.tweeted == False:
                print 'Tweeting!'
                msg = GET_TEXT.format(board=board.board, time_until=int(min_until), get_name=GET_name(board.next_GET), posts_to_go=int(posts_to_go)).capitalize()
                twitter.update_status(msg)  #could add another tweepy error handler
                print msg
            else:
                print 'Already tweeted.'
        sleep(2)    #to meet 4chan API timing standards
    print 'Sleeping 10 minutes...'
    sleep(10*60)

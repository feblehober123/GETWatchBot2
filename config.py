### CONFIG VARS
# moved here to be accessible to all files 
HOURS_HUMAN_TWEET_IS_RELEVANT = 1
DAYS_NEW_BOARD_IS_FRESH    = 2     #Days after creation of a board that the bot will still tweet about the new board
MINUTES_GET_IS_SOON        = 20    #Time in minutes before the GET that the bot will try to tweet at
MINUTES_GET_IS_UPON_US     = 5     #Time in minutes before the GET that it is basically occuring already
HOURS_HUMAN_TWEET_IS_RELEVANT = 1   #The bot will not tweet about a GET if a human has tweeted about it within this many hours
NON_DUBS_BOARDS = ['b', 'v', 'vg', 'vr']    #boards that do not have dubs, may need to be updated in the future

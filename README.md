GETWatchBot2
============

Formerly _xXxG3T\_W4T<H\_B0T\_R3L40D3D\_4.20xXx_, GETWatchBot2 is the newer and (hopefully) more complete and less buggy version of the original GETWatchBot.
The GETWatchBot is a bot for [@GETWatch](http://twitter.com/GETWatch), by Kabo-chan.

The GETWatchBot will automatically tweet about upcoming GETs 45 minutes before they happen. This will cut out a lot of work for the humans, because they should no longer have to manually check when GETs are occuring and tweet about them.
However, if a human has tweeted about the GET, the bot will not post and defer to the human since humans are more social than bots. It will also tweet about new boards.

Installation
------------

Experience has shown that I may not always be able to keep the GETWatchBot online, so I have tried to simplify some things to enable other people to be able to run the bot when I cannot, as long as they have the OAuth keys for twitter (ask the owners of @GETWatch).

The GETWatchBot uses the external libraries tweepy and requests. You can install them with

`$ pip install tweepy requests` 

assuming you are on a Unix-like system, but if you aren't, you probably won't be able to use the bot anyway without recompiling repdigits.c (see repdigits_setup.py).

The oauth.py script is useful for obtaining the access key/secret, which should be placed in oauth.conf

repdigits.so was compiled on an amd64 architechture. If your processor is not amd64, you will need to recompile it with the simple repdigits_compile.sh script. This requires gcc.

Requirements
------------

* Python 2.7 (2.x might work)
* requests
* tweepy

Again, you can install them with

`$ pip install requests tweepy`

Usage
-----

To run the bot, execute the file main.py or run.py
The run.py script is a wrapper around main.py that restarts the bot when it crashes and logs errors to errors.log. Either will execute the bot, but main.py will not keep it up when it crashes.

Contributing
------------

If there is something you would like to contribute to the bot, please do, it can use all the help it can get. Even if you have just determined that the bot is not running, or that it did not tweet about a GET, please contact me through [email](mailto:kabochan222@gmail.com). If you have decided to run the bot because I cannot, please email me first, but if I do not respond in a while you are free to assume that I am MIA.

Credits
-------

ALL ME!!!!1 (me = --> Kabo-chan <\--)

Notes
-----

This bot is (probably) buggy, but hopefully less buggy than the original, otherwise I wasted my time on rewriting it/scrapping it together. It may not always work, especially if the 4chan API changes.

TO DO: 

* Automatically initialize new boards and append them to the list of GET classes
* Add error loggers for caught exceptions in GET.py

License
-------

This code is licensed as FREE SOFTWARE under the GNU GPLv3

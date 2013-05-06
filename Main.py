# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
from ConfigParser import SafeConfigParser
from setuptools import setup, Extension

import twitterGetter

usage = """

twitterGetter - twitter-log implementation for TwitterManager

reference: twitter-log - Twitter Logger/Archiver

USAGE:

    Main.py <screen_name> [max_id]

DESCRIPTION:

    insert <screen_name>'s tweets into a database for 
TwitterManager frontend.
    
    max_id may be provided to ignore previously downloaded tweets 
and avoid multiple downloads.

"""




def fetchTwitts(username):
    
    database, options = get_setup()
    option_verbose = enabled(options, 'verbose')
    
    twitterUserName = username
    
    twits = twitterGetter.twitterGetter()
    
    twits.set_config(verbose=option_verbose,host=database['host'],port=database['port'],user=database['dbuser'],passwd=database['passwd'],db=database['dbname'])
    
    twits.screen_name = twitterUserName
    
    twits.get(twitterUserName)

    return twits.n_tweets

def get_setup():
    config = SafeConfigParser()
    config.read(['setup.cfg'])
    
    options = dict(config.items('options'))
    database = dict(config.items('database'))
    
    return database, options

def enabled(options, option):
    value = options[option]
    s = value.lower()
    if s in ('yes','true','1','y'):
        return True
    elif s in ('no', 'false', '0', 'n'):
        return False
    else:
        raise ValueError("Unknown value %s for option %s" % (value, option))

def main():
    
    if len(sys.argv) != 2:
        print(usage)
        return 1
     
    tweets_count = fetchTwitts(sys.argv[1])
    print("tweets_count:",tweets_count)
    return 0
    
if __name__ == "__main__":
    main()
    sys.exit()
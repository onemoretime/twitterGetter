# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
from ConfigParser import SafeConfigParser

import twitterGetter

usage = """

twitterGetter - twitter-log implementation for TwitterManager

reference: twitter-log - Twitter Logger/Archiver

USAGE:

    Main.py {(-t|--token <token> -ts|--token-secret <token secret>) | -tcfg } [-m|--max-id=<max_id>] [--quiet] <screen_name> 

DESCRIPTION:

    --t|--token <token> -ts|--token-secret <token secret> are mandatory since the forced usage of API 1.1
    -tcfg indicates that token informations are in cfg file (twitter_credentials section)

    insert <screen_name>'s tweets into a database for 
TwitterManager frontend.
    
    -m|--max_id is optional and may be provided to ignore previously downloaded tweets 
and avoid multiple downloads.
    --quiet indicates very few output 
"""




def fetchTwitts(username,lastid=None, oauth=None,oauth_secret=None,consumer=None, consumer_secret=None):
    
    database, options, twitter_credentials = get_setup()
    option_verbose = enabled(options, 'verbose')
    
    if ( ( consumer == None ) & ( consumer_secret == None ) ):
        if (option_verbose == 1):
            print("twitter_credential_token: %s" % twitter_credentials['consumer'])
        # token are not send in commandline, fi we arrive here, then token are in config file.
        oauth_token = twitter_credentials['oauth_token']
        oauth_secret = twitter_credentials['oauth_secret']
        consumer = twitter_credentials['consumer']
        consumer_secret = twitter_credentials['consumer_secret']
    
    ###############
    # Add checks on tokens
    ###############
    
    twitterUserName = username
    max_id=lastid
    #oauth_token,oauth_token_secret,CONSUMER_KEY,CONSUMER_SECRET
    twits = twitterGetter.twitterGetter(oauth_token,oauth_secret,consumer, consumer_secret)
    
    twits.set_config(verbose=option_verbose,host=database['host'],port=database['port'],user=database['dbuser'],passwd=database['passwd'],db=database['dbname'])
    
    twits.screen_name = twitterUserName
    
    twits.get(twitterUserName,max_id)

    return twits.n_tweets

def get_setup():
    config = SafeConfigParser()
    config.read(['setup.cfg'])
    
    options = dict(config.items('options'))
    database = dict(config.items('database'))
    creds = dict(config.items('twitter_credentials'))
    
    return database, options, creds

def enabled(options, option):
    value = options[option]
    s = value.lower()
    if s in ('yes','true','1','y'):
        return True
    elif s in ('no', 'false', '0', 'n'):
        return False
    else:
        raise ValueError("Unknown value %s for option %s" % (value, option))

def main(args=sys.argv[0:]):
    max_id = None
    verbose = 1
    screenName = None
    consumer = None
    consumer_secret = None
    oauth = None
    oauth_secret = None
    if not args:
        print("Error: Not enough args")
        print(usage)
        return 1
    if args[1:]:
        arglen = len(args[1:])
        print(arglen)
        # for i=0, args = source file
        i = 1

        while (i < arglen+1):
            print("arg %s: %s" % (i,args[i])) 
            if ((args[i] == '-t') or (args[i] == '--consumer')):
                consumer = args[i+1]
                i=i+2
            elif ((args[i] == '-ts') or (args[i] == '--consumer-secret')):
                consumer_secret = args[i+1]
                i=i+2
            elif ((args[i] == '-m') or (args[i] == '--max-id')):
                max_id = args[i+1]
                i=i+2
            elif (args[i] == '-tcfg'):
                # token are in cfonfig file
                consumer = None
                consumer_secret = None
                i = i + 1
            elif (args[i] == '--quiet'):
                verbose = 0
                i = i + 1
            else:
                screenName = args[i]
                i = i + 1
    if (verbose == 1):
        print ("Token: %s" % consumer)
        print ("Token_Secret: %s" % consumer_secret)
        print ("Max_ID: %s" % max_id)
        print ("ScreenName: %s" % screenName)
    if ((screenName == None) & verbose):
        print ("You have to specify a ScreenName")
        return 1
    
    ###########
    # Add verif on parameters or a better way to set parameters
    ###########
    
    tweets_count = fetchTwitts(screenName,max_id,oauth,oauth_secret,consumer,consumer_secret)
    print("tweets_count:",tweets_count)
    return 0
    
if __name__ == "__main__":
    main()
    sys.exit()
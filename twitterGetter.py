# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
import re


import MySQLdb
import _mysql_exceptions


from twitter.api import Twitter, TwitterError
from twitter.cmdline import CONSUMER_KEY, CONSUMER_SECRET
from twitter.auth import NoAuth
from twitter.util import printNicely

class twitterGetter:

    def __init__(self):
        self.twitter = Twitter(
            auth=NoAuth(),
            api_version='1',
            domain='api.twitter.com')
        self.screen_name=""
        self.max_id=None
        self.n_tweets = 0
        self.debug = 0 # if set, go verbose
        self.dbconn = None
        self.host = "localhost"
        self.port = 0
        self.user = "username"
        self.passwd = "password"
        self.db = "dbname"
        
    def set_config(self,verbose=None,host=None,port=None,user=None,passwd=None,db=None):
        if not verbose == None: self.debug = verbose
        if not host == None: self.host = host
        if not user == None: self.user = user
        if not passwd == None: self.passwd = passwd
        if not db == None: self.db = db
        if not port == None: self.port = port
        
    def get_raw(self,screen_name,max_id=None):
        # provide same working mode as direct use of twitter-log
        while True:
            try:
                tweets_processed, max_id = self.get_tweets_raw(self.twitter, self.screen_name, self.max_id)
                self.n_tweets += tweets_processed
                if self.debug: self.log_debug("Processed %i tweets (max_id %s)" %(self.n_tweets, max_id))
                if tweets_processed == 0:
                    if self.debug: self.log_debug("That's it, we got all the tweets. Done.")
                    break
            except TwitterError as e:
                if self.debug: self.log_debug("Twitter bailed out. I'm going to sleep a bit then try again")
                if self.debug: self.log_debug("%s" % e)
                time.sleep(3)
    
 
    def log_debug(self,msg):
        print(msg, file=sys.stderr)
    
    def get_tweets_raw(self,twitter, screen_name, max_id=None):
        # provide same working mode as direct use of twitter-log
        kwargs = dict(count=3200, screen_name=screen_name)
        if max_id:
            kwargs['max_id'] = max_id
        n_tweets = 0
        tweets = twitter.statuses.user_timeline(**kwargs)
        for tweet in tweets:
            if tweet['id'] == max_id:
                continue
            print("%s %s\nDate: %s" % (tweet['user']['screen_name'],
                                       tweet['id'],
                                       tweet['created_at']))
            if tweet.get('in_reply_to_status_id'):
                print("In-Reply-To: %s" % tweet['in_reply_to_status_id'])
            print()
            for line in tweet['text'].splitlines():
                printNicely('    ' + line + '\n')
            print()
            print()
            max_id = tweet['id']
            n_tweets += 1
        return n_tweets, max_id
    
    
###################################
# add tweets in DB
###################################

    def get(self,screen_name,max_id=None):   
        while True:
            try:
                if self.debug: 
                    print ("passed arguments :")
                    print ("  screnname : " , self.screen_name)
                    print ("  max_id : " , self.max_id)                        
                tweets_processed, self.max_id = self.get_tweets(self.twitter, self.screen_name, self.max_id)
                self.n_tweets += tweets_processed
                if self.debug: self.log_debug("Processed %i tweets (max_id %s)" %(self.n_tweets, max_id))
                if tweets_processed == 0:
                    if self.debug: self.log_debug("That's it, we got all the tweets. Done.")
                    break                
            except TwitterError as e:
                if self.debug:
                    self.log_debug("Twitter bailed out. I'm going to sleep a bit then try again")
                    self.log_debug("%s" % e)                
            
    def get_tweets(self,twitter,screen_name,max_id=None):
        kwargs = dict(count=3200, screen_name=screen_name)
        if max_id:
            kwargs['max_id'] = max_id
        n_tweets = 0
        try:
            conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db)
        except _mysql_exceptions, e:
            if self.debug: self.log_debug("%s" % e)       
        # find SQL id for screen_name
        if self.debug: print("Connected to mysqldb")
        x = conn.cursor()
        try:
            x.execute("SELECT idxTwitterUserName FROM TwitterUserName WHERE screename = '%s'" % screen_name)
            strUserInTreatment = x.fetchone()
            x.close()
        except _mysql_exceptions, e:
            if self.debug: self.log_debug("%s" % e)
            conn.close()
            sys.exit()


        tweets = twitter.statuses.user_timeline(**kwargs)

        for tweet in tweets:
            if tweet['id'] == max_id:
                continue
            #Sanitization of datas in tweet['text']
            data = ""
            for line in tweet['text'].splitlines():
                data = data + re.escape(line)
            # Date traitement In: Wed Mar 20 14:47:55 +0000 2013 Out: AAAA-MM-JJ HH:MM:SS
            strdate = time.strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y")
            sqldate = time.strftime('%Y-%m-%d %H:%M:%S',strdate)
            
            x = conn.cursor()
            try:
                # sanitization of datas : permit encoding of some unicode chars, ...
                data = data.encode("iso-8859-15", "xmlcharrefreplace")
                if isinstance(data, str):
                    data = unicode(data, 'ascii',errors='ignore')
                x.execute("INSERT IGNORE INTO tweets SET idtweet=%s,tweetContent=%s,tweetDate=%s" , (tweet['id'],data,sqldate))
                conn.commit()
                lastinsert = x.lastrowid
                # update table relation
                if lastinsert > 0:
                    x.execute("INSERT IGNORE INTO TwitterUserName_has_tweets SET TwitterUserName_idxTwitterUserName=%s,tweets_idxTweets=%s" , (int(strUserInTreatment[0]),lastinsert))
                    conn.commit()
            except _mysql_exceptions, e:
                if self.debug: self.log_debug("%s" % e)
                conn.rollback()
            max_id = tweet['id']
            n_tweets += 1
            x.close()
        
        x = conn.cursor()
        x.execute("UPDATE TwitterUserName SET TwitterUserNameLastTweetID=%s WHERE idxTwitterUserName=%s" , (int(max_id),int(strUserInTreatment[0])))
        conn.commit()            
        conn.close()
        if self.debug:
            print ("Returned args :")
            print ("  Returned max_id : " , max_id)
            print ("  Returned n_tweets  : ", n_tweets)
        
        return n_tweets, max_id
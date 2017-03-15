""" Streaming twitter API"""

from __future__ import print_function
import sys
import tweepy
import json
import csv
import re
import numpy as np
from ConfigParser import ConfigParser
from nltk.corpus import stopwords
import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for,session,jsonify,request, redirect


DATABASE= '/Users/ruchapitke/Desktop/web/web.db'

import sqlite3
conn = sqlite3.connect('web.db')
c = conn.cursor()

 
class TwitterListener(tweepy.StreamListener):
    """ Twitter stream listener. """
    def __init__(self, api=None):
        super(TwitterListener, self).__init__()
        self.num_tweets = 0
        self.list_of_tweets = []

    def on_status(self, status):
        tweet_info = []
        record = status.text
       # print (record)
        tweet_info.append(record)
        user = status.user.screen_name
        tweet_info.append(user)
        followers = status.user.followers_count
        tweet_info.append(followers)
        retweet_count = status.retweet_count
        tweet_info.append(retweet_count)

       
        c.execute('INSERT INTO TWITTER(HEADLINE, USER_NAME, FOLLOWER_COUNT, TWEET_TEXT, RETWEET_COUNT,STATUS) VALUES(?,?,?,?,?,?)', (word,user,followers,record,retweet_count,False))

        conn.commit()

        self.num_tweets += 1
        if self.num_tweets < 100:
            self.list_of_tweets.append(tweet_info)
            return True
        else:
            return False

    def on_error(self, msg):
        print('Error: %s', msg)

    def on_timeout(self):
        print('timeout : wait for next poll')
        sleep(10)

def get_config():
    """ Get the configuration """
    conf = ConfigParser()
    conf.read('config.cfg')
    return conf

def get_stream():
    config = get_config()
    auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'),
                               config.get('twitter', 'consumer_secret'))

    auth.set_access_token(config.get('twitter', 'access_token'),
                          config.get('twitter', 'access_token_secret'))

    listener = TwitterListener()
    stream = tweepy.Stream(auth=auth, listener=listener)
    return stream

def clean_tweets(tweet_list):
    clean_tweet_list = []
    for tweet in tweet_list:
    #tweet = re.sub('^RT','',tweet)
    #tweet = re.sub('@[a-zA-Z0-9]*:','',tweet)
    #tweet = re.sub('\\[a-zA-Z]','',tweet).replace('\u','').replace('\\','').replace('@','').replace('-',' ')
    #tweet = re.sub('http.*','',tweet)
    #tweet = re.sub('\.+','',tweet)
    #tweet = re.sub('[^a-zA-Z0-9-_*.]', ' ', tweet)
    #tweet = re.sub('[0-9]','',tweet)
    #tweet = ' '.join(tweet.split())
        clean_tweet_list.append(tweet)
        return clean_tweet_list

if __name__ == "__main__":
    #if len(sys.argv) != 2:
        #print("Usage: %s <word>" % (sys.argv[0]))
    #else:
        #word = sys.argv[1]
    word = "trump"
    stream = get_stream()
    print("Listening to '%s' and '%s' ..." %('#' + word, word)) 
    stream.filter(track=['#' + word, word])
    cleaned_tweets = clean_tweets(stream.listener.list_of_tweets)
    filename = word + '_tweets.txt'
    file = open(filename, 'w+')
    file.write(str(cleaned_tweets))
    file.close()


conn.close()

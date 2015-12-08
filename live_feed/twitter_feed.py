from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from StringIO import StringIO
import simplejson
import json
import pprint
import tweepy
from ConfigParser import *
import sentiment
import mongo_doc 
import pymongo

hashes = ''

def read_config():
    parser = SafeConfigParser()
    global hashes
    parser.read('social_media.config')
    access_token = parser.get('Twitter','access_token')
    access_secret = parser.get('Twitter','access_secret')
    consumer_key = parser.get('Twitter','consumer_key')
    consumer_secret = parser.get('Twitter','consumer_secret')
    if not parser.get('General', 'hashes'):
        hashes = parser.get('Twitter', 'hashes')
    else:
        hashes = parser.get('General', 'hashes')
        print "Got general hashes"
    if len(access_token)!=50:
        print "Looks like you have an invalid access token here, please check"
        return -1
    return access_token,access_secret,consumer_key,consumer_secret

def get_tweets():
    access_token,access_secret,consumer_key,consumer_secret = read_config()
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    global hashes
    count = 0
    api = tweepy.API(auth)
    hashes = hashes.replace("'","").split(",")
    for hashtag in hashes:
        tweets = api.search(hashtag)
        for tweet in tweets:
            #print tweet.text
            twitter_json = {}
            twitter_json["created_at"] = str(tweet.created_at)
            twitter_json["caption"] = tweet.text
            twitter_json["username"] = tweet.user.name
            twitter_json["thumbs"] = sentiment.check_sentiments(tweet.text)
            twitter_json["source"] = "twitter"
            twitter_json["link"] = "https://twitter.com/"+str(tweet.user.screen_name)+"/status/"+str(tweet.id)
            print twitter_json["link"]
            if 'media' in tweet.entities:
                twitter_json["url"] = tweet.entities['media'][0]['media_url']
            else:
                twitter_json["url"] = ""
            push_mongo(twitter_json)

def push_mongo(tweet_json):
    mongo = mongo_doc.MongoOP()
    mongo.store_values(tweet_json)
    
if __name__ == '__main__':
    get_tweets()

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
import apiclient.discovery
from apiclient.discovery import build

hashes = ''

def read_config():
    parser = SafeConfigParser()
    global hashes
    parser.read('social_media.config')
    API_KEY = parser.get('Google+','api_key')
    if not parser.get('General', 'hashes'):
        hashes = parser.get('Google+', 'hashes')
    else:
        hashes = parser.get('General', 'hashes')
        #print "Got general hashes"
    return API_KEY

def get_posts():
    global hashes
    plus = build('plus', 'v1', developerKey=read_config())
    hashes = hashes.replace("'","").split(",")
    for hashtag in hashes:
        posts = plus.activities().search(query=hashtag).execute().get('items', [])
        for post in posts:
            gplus_json = {}
            #print hashtag
            print json.dumps(post)
            gplus_json['created_at'] = str(post['published']) #.encode('ascii','ignore')
            gplus_json['link'] = post['url']
            gplus_json['url'] = post['object']['attachments'][0]['image']['url']
            gplus_json['caption'] =post['object']['content']
            gplus_json['username'] = post['actor']['displayName']
            gplus_json['sentiment'] = 'thumbs-up'
            gplus_json['source'] = 'Google+'
            push_mongo(gplus_json)

def push_mongo(gplus_json):
    mongo = mongo_doc.MongoOP()
    mongo.store_values(gplus_json)
    
if __name__ == '__main__':
    get_posts()

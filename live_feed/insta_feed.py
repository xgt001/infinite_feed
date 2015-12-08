from instagram.client import InstagramAPI
import instagram
import json
from ConfigParser import SafeConfigParser
import sentiment
import mongo_doc
import pymongo
from mongo_doc import MongoDoc,MongoOP

tags = ''

def read_config():
    parser = SafeConfigParser()
    global tags
    parser.read('social_media.config')
    access_token = parser.get('Instagram','access_token')
    if not parser.get('General', 'hashes'):
        tags = parser.get('Instagram', 'tags')
    else:
        tags = parser.get('General', 'hashes')
    if len(access_token)!=50:
        print "Looks like you have an invalid access token here, please check"
        return -1
    return access_token

def get_instagram_posts():
    api = InstagramAPI(access_token=read_config())
    global tags
    tags = tags.replace("'","").split(',')
    for tag in tags:
        print tag
        filtered_media, barr = api.tag_recent_media(count=100,max_id=1,tag_name=tag)
        #print filtered_media
        for media in filtered_media:
            insta_json = {}
            insta_json['url']=str(media.images['standard_resolution'].url)
            insta_json['created_at']=str(media.created_time)
            insta_json['username']=str(media.user.username)
            insta_json['link']=str(media.link)
            insta_json['caption']=str(media.caption)
            insta_json['thumbs']=str(sentiment.check_sentiments(insta_json['caption']))
            insta_json['source']="instagram"
            #print "json"+str(insta_json)
            mongo = mongo_doc.MongoOP()
            mongo.store_values(insta_json)

def push_mongo(insta_json):
    mongo = mongo_doc.MongoOP()
    mongo.store_values(insta_json)

if __name__ == '__main__':
    get_instagram_posts()

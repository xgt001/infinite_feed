from flask import Flask
import ast
from flask import request
from facebook_feed import FacebookFeed
from mongo_doc import MongoDoc, MongoOP
from flask import Blueprint

facebook = Blueprint('facebook', __name__)

@facebook.route("api/ul3livefeed", methods=['GET', 'POST'])
def get_feed():
    if request.method == 'POST':
        result = request.get_json()
        result = result['entry'][0]
        fb_feed = FacebookFeed(result)
        feed = fb_feed.compose_json()
        mongo_conn = MongoOP()
        mongo_conn.store_values(feed)
        return "200 OK"
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "ul3livefeed":
            return request.args.get('hub.challenge')

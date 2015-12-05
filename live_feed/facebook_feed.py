import datetime
import sys
from senti_analysis import check_sentiments


class FacebookFeed(object):
    def __init__(self, fb_feed):
        self.feed = fb_feed

    def convert_time(self, time):
        return datetime.datetime.fromtimestamp(int(1449237434)).strftime('%Y-%m-%d %H:%M:%S')

    def validate_key(self, feed, key):
        if feed.has_key(key):
            return str(feed[key])
        else:
            return ""

    def compose_json(self):
        try:
            time = self.convert_time(self.feed['time'])
            feed = self.feed['changes'][0]['value']
            caption = self.validate_key(feed, "message")
            split_id = self.validate_key(feed, "post_id").split('_')
            user_id = split_id[0]
            post_id = split_id[1]
            link = "https://www.facebook.com/{}/posts/{}".format(user_id, post_id) 
            thumbs = check_sentiments(caption)
            username = self.validate_key(feed, "sender_name")
            url = self.validate_key(feed, "link")
            final_feed = {'created_at': time,
                          'caption': caption,
                          'link': link,
                          'thumbs': thumbs,
                          'source': "facebook",
                          'username': username,
                          'url': url}
            return final_feed
        except KeyError as ERR:
            print "error is".format(ERR)
            sys.exit(1)


import requests
import json

def check_sentiments(message):
    try:
        request = requests.post("http://text-processing.com/api/sentiment/", data = {"text":message})
        sentiment = json.loads(request.content)['label']
        if sentiment == "pos":
            return "thumbs-up"
        else:
            return "thumbs-down"
    except requests.exceptions as err:
        print "Error with sentiment requests" + r

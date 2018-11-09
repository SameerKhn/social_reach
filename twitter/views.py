from django.shortcuts import render
from tweepy import Cursor
from . import authentication
import json
from collections import Counter

# Create your views here.

def index(request):
    client = authentication.get_twitter_client()
    list=[]
    hashtagList=[]
    hashtags = Counter()
    user ='ZAbbasOfficial'

    for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(3):
       for status in page:
         list.append(json.dumps(status._json)+"\n")

    for line in list:
        tweet = json.loads(line)
        hashtagsInTweet = authentication.get_hashtags(tweet)
        hashtags.update(hashtagsInTweet)

    for tag in hashtags.most_common(20):
        hashtagList.append(tag)

    context = {'status': hashtagList}
    return render(request, 'twitter/index.html', context)

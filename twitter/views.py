from django.shortcuts import render
from tweepy import Cursor
from . import authentication
import json
from collections import Counter
from collections import defaultdict

# Create your views here.



def index(request):
    client = authentication.get_twitter_client()
    list=[]
    hashtagList=[]
    hashtags = Counter()
    #Dictionary={}
    percentEliteList=[]
    user ='PacktPub'
    hashtag_count = defaultdict(int)

    for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(3):
       for status in page:
         list.append(json.dumps(status._json)+"\n")

    for line in list:
        tweet = json.loads(line)
        hashtagsInTweet = authentication.get_hashtags(tweet)
        hashtags.update(hashtagsInTweet)
        n_of_hashtags = len(hashtagsInTweet)
        hashtag_count[n_of_hashtags] += 1

    for tag in hashtags.most_common(20):
        hashtagList.append(tag)

    # Dictionary = authentication.NoOfHashtags(list,hashtagsInTweet)
    #hashtagPercentListElite = authentication.HashtagsWithPercentElite()
    tweetsNoOfHashtags, tweetsNo_Of_Hashtags_with_percent, tweetsWithHashtags,tweets_with_hashtags_percent,percentEliteList=authentication.NoOfHashtags(n_of_hashtags,hashtag_count)

    context = {'status': hashtagList, 'tweetsNoOfHashtags':tweetsNoOfHashtags,'tweetsNo_Of_Hashtags_with_percent':tweetsNo_Of_Hashtags_with_percent,
               'tweetsWithHashtags':tweetsWithHashtags, 'tweets_with_hashtags_percent':tweets_with_hashtags_percent,'percentEliteList':percentEliteList}
    return render(request, 'twitter/index.html', context)

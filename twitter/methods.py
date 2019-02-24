from nltk.tokenize import TweetTokenizer
from tweepy import Cursor
from . import authentication
from collections import Counter
import math
import json
import time


users = Counter()
FollowerList = []
FriendList= []
client = authentication.get_twitter_client()
MAX_FRIENDS = 15000
max_pages = math.ceil(MAX_FRIENDS / 5000)

#Getting the Hashtags
def get_hashtags(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]

#Getting No. Of Hashtags
def NoOfHashtags (noOfTags , hashtagCount):
    percentEliteList = []
    tweetsWithHashtags= sum([count for noOfTags, count in hashtagCount.items() if noOfTags > 0])
    tweetsNoOfHashtags = hashtagCount[0]
    tweetsTotal = tweetsNoOfHashtags + tweetsWithHashtags
    tweets_with_hashtags_percent  = "%.2f" % (tweetsWithHashtags / tweetsTotal*100)
    tweetsNo_Of_Hashtags_with_percent = "%.2f" % (tweetsNoOfHashtags / tweetsTotal*100)

    for tag_count, tweet_count in hashtagCount.items():
        if tag_count > 0:
            percent_total = "%.2f" % (tweet_count / tweetsTotal * 100)
            percent_elite = "%.2f" % (tweet_count / tweetsWithHashtags * 100)
            #print("{} tweets with {} hashtags ({}% total, {}% elite)".format(tweet_count, tag_count,percent_total,percent_elite))
            tempList=[tweet_count,tag_count,percent_total,percent_elite]
            percentEliteList.append(tempList)

    return (tweetsNoOfHashtags, tweetsNo_Of_Hashtags_with_percent, tweetsWithHashtags, tweets_with_hashtags_percent,percentEliteList)

#Getting User Mentions
def get_mentions(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('user_mentions', [])
    return [tag['screen_name'] for tag in hashtags]

#Getting Term Frequencies
def TermFrequencyProcess(text,tokenizer= TweetTokenizer(),stopWords=[]):
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return [tok for tok in tokens if tok not in stopWords and not tok.isdigit()]

#For pagination of items
def paginate(items, n):
    """Generate n-sized schunks from items"""
    for i in range(0, len(items), n):
        yield items[i:i+n]

#Getting Followers of  user
def GetFollowers(screen_name):
    # get followers for a given user

    for followers in Cursor(client.followers_ids, screen_name=screen_name).pages(max_pages):
        for chunk in paginate(followers, 100):
            users = client.lookup_users(user_ids=chunk)
            for user in users:
                FollowerList.append(json.dumps(user._json) + "\n")
        if len(followers) == 5000:
            # print("More results available. Sleeping for 60 seconds to avoid rate limit")
            time.sleep(60)

    return FollowerList

#Getting Followers of  user
def GetFreinds(screen_name):
    # get friends for a given user
    for friends in Cursor(client.friends_ids, screen_name=screen_name).pages(max_pages):
        for chunk in paginate(friends, 100):
            users = client.lookup_users(user_ids=chunk)
            for user in users:
                FriendList.append(json.dumps(user._json) + "\n")
        if len(friends) == 5000:
            # print("More results available. Sleeping for 60 seconds to avoid rate limit")
            time.sleep(60)

    return FriendList

def GetUserProfile(screen_name):
    # get user's profile
    profile = client.get_user(screen_name=screen_name)
    UserProfile = (json.dumps(profile._json, indent=4))
    return UserProfile

def FriendAndFollowerNames(FollowerList=[] ,FriendList=[]):
    FollowerNames = []
    FreindNames = []
    for line in FollowerList:
        profile = json.loads(line)
        FollowerNames.append(profile['screen_name'])
    for line in FriendList:
        profile = json.loads(line)
        FreindNames.append(profile['screen_name'])

    mutual_friends = [user for user in FreindNames if user in FollowerNames]
    followers_not_following = [user for user in FollowerNames if user not in FreindNames]
    friends_not_following = [user for user in FreindNames if user not in FollowerNames]

    return mutual_friends,followers_not_following,friends_not_following,len(FreindNames),len(FollowerNames)

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
from tweepy import Cursor
from . import authentication
from collections import Counter
import math
import json
import time
from collections import defaultdict
from textblob import TextBlob

MAX_FRIENDS = 15000
max_pages = math.ceil(MAX_FRIENDS / 5000)

#Model For The Integrating Tag And Count
class HashtagModel:
    def __init__(self,tag,count):
        self.tag=tag
        self.count=count

#Getting the Hashtags
def get_hashtags(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]

#Getting No. Of Hashtags
def NoOfHashtags (statusList=[]):
    percentEliteList = []
    hashtag_count = defaultdict(int)
    for line in statusList:
        tweet = json.loads(line)
        hashtags_in_tweet = get_hashtags(tweet)
        n_of_hashtags = len(hashtags_in_tweet)
        hashtag_count[n_of_hashtags] += 1
    tweetsWithHashtags= sum([count for noOfTags, count in hashtag_count.items() if noOfTags > 0])
    tweetsNoOfHashtags = hashtag_count[0]
    tweetsTotal = tweetsNoOfHashtags + tweetsWithHashtags
    tweets_with_hashtags_percent  = "%.2f" % (tweetsWithHashtags / tweetsTotal*100)
    tweetsNo_Of_Hashtags_with_percent = "%.2f" % (tweetsNoOfHashtags / tweetsTotal*100)

    for tag_count, tweet_count in hashtag_count.items():
        if tag_count > 0:
            percent_total = "%.2f" % (tweet_count / tweetsTotal * 100)
            percent_elite = "%.2f" % (tweet_count / tweetsWithHashtags * 100)
            #print("{} tweets with {} hashtags ({}% total, {}% elite)".format(tweet_count, tag_count,percent_total,percent_elite))
            tempList=[tweet_count,tag_count,percent_total,percent_elite]
            percentEliteList.append(tempList)

    return (tweetsNoOfHashtags, tweetsNo_Of_Hashtags_with_percent, tweetsWithHashtags, tweets_with_hashtags_percent,percentEliteList)

# Get Top 5 Tweets From user timeline
def GetTopTweets(statusList=[]):
    tweetList=[]
    for number in range(5):
        tweet = json.loads(statusList[number])
        text= tweet.get('text')
        date= tweet.get('created_at')
        object = HashtagModel(text, date)
        tweetList.append(object)
    return tweetList


#Top 10 Hashtags
def CalculatingHashtags(statusList=[]):
    hashtags = Counter()
    ListOfDicts=[]

    for line in statusList:
        tweet = json.loads(line)
        hashtags_in_tweet = get_hashtags(tweet)
        hashtags.update(hashtags_in_tweet)
    for tag,count in hashtags.most_common(10):
        object=HashtagModel(tag,count)
        ListOfDicts.append(object)

    return ListOfDicts

#Processing User Mentions
def get_mentions(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('user_mentions', [])
    return [tag['screen_name'] for tag in hashtags]

#Getting User Mentions
def GetUserMentions(statusList=[]):
    users = Counter()
    UserMentionList=[]
    for line in statusList:
        tweet = json.loads(line)
        mentions_in_tweet = get_mentions(tweet)
        users.update(mentions_in_tweet)
    for user, count in users.most_common(10):
        object = HashtagModel(user, count)
        UserMentionList.append(object)
    return UserMentionList

#Processing Term Frequencies
def TermFrequencyProcess(text,tokenizer= TweetTokenizer(),stopWords=[]):
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return [tok for tok in tokens if tok not in stopWords and not tok.isdigit()]

#Getting The Top 10 Most Used Words By User
def GetTermFrequency(statusList=[]):
    ObjectList=[]
    tweet_tokenizer=TweetTokenizer()
    punct = list(string.punctuation)
    stopword_list = stopwords.words('english') + punct + ['rt','@', 'via', '...']
    tf = Counter()
    for line in statusList:
        tweet = json.loads(line)
        tokens = TermFrequencyProcess(tweet['text'], tweet_tokenizer, stopword_list)
        tf.update(tokens)
    for tag, count in tf.most_common(10):
        object=HashtagModel(tag,count)
        ObjectList.append(object)
    return ObjectList

#For pagination of items(Generate n-sized schunks from items)
def paginate(items, n):

    for i in range(0, len(items), n):
        yield items[i:i+n]

#Getting Followers of  user
def GetFollowers(screen_name):
    # get followers for a given user
    users = Counter()
    FollowerList = []
    client = authentication.get_twitter_client()
    for followers in Cursor(client.followers_ids, screen_name=screen_name).pages(max_pages):
        for chunk in paginate(followers, 100):
            users = client.lookup_users(user_ids=chunk)
            for user in users:
                FollowerList.append(json.dumps(user._json) + "\n")
        if len(followers) == 5000:
            # print("More results available. Sleeping for 60 seconds to avoid rate limit")
            time.sleep(60)

    return FollowerList

#Getting Freinds of  user
def GetFreinds(screen_name):
    # get friends for a given user
    users = Counter()
    FriendList = []
    client = authentication.get_twitter_client()
    for friends in Cursor(client.friends_ids, screen_name=screen_name).pages(max_pages):
        for chunk in paginate(friends, 100):
            users = client.lookup_users(user_ids=chunk)
            for user in users:
                FriendList.append(json.dumps(user._json) + "\n")
        if len(friends) == 5000:
            # print("More results available. Sleeping for 60 seconds to avoid rate limit")
            time.sleep(60)

    return FriendList

#Getting User Profile
def GetUserProfile(screen_name):
    # get user's profile
    client = authentication.get_twitter_client()
    profile = client.get_user(screen_name=screen_name)
    UserProfile = (json.dumps(profile._json, indent=4))
    return UserProfile

#Getting User Timeline
def GetUserTimeline(screen_name):
    client = authentication.get_twitter_client()
    statusList = []
    for page in Cursor(client.user_timeline, screen_name=screen_name, count=200).pages(30):
        for status in page:
            statusList.append(json.dumps(status._json) + "\n")

    return statusList

#Freinds And Followers Analysis
def FriendAndFollowerNames(FollowerList=[] ,FriendList=[]):
    FollowerNames = set()
    FreindNames = set()
    for line in FollowerList:
        profile = json.loads(line)
        FollowerNames.add(profile['screen_name'])
    for line in FriendList:
        profile = json.loads(line)
        FreindNames.add(profile['screen_name'])

    mutual_friends = FreindNames.intersection(FollowerNames)
    followers_not_following = FollowerNames.difference(FreindNames)
    friends_not_following = FreindNames.difference(FollowerNames)

    return len(mutual_friends),len(followers_not_following),len(friends_not_following),len(FreindNames),len(FollowerNames)

#Sentiment Analysis Function
def performAnalysis(statusList=[]):
    positive,negative,neutral = 0,0,0
    list = []
    PostiveTweets,NeutralTweets,NegativeTweets=[],[],[]
    for tweet in statusList:
         Tweet=json.loads(tweet)
         analysis = TextBlob(Tweet.get('text'))
         if analysis.sentiment.polarity > 0:
            positive = positive+1
            PostiveTweets.append(Tweet.get('text'))

         if analysis.sentiment.polarity < 0:
            negative = negative +1
            NegativeTweets.append(Tweet.get('text'))

         if analysis.sentiment.polarity == 0:
             neutral = neutral + 1
             NeutralTweets.append(Tweet.get('text'))

    list.append(positive)
    list.append(negative)
    list.append(neutral)
    return list,PostiveTweets,NeutralTweets,NegativeTweets

#Get Analysis of Influence And Engagement
def InfluenceAndEngagement(UserProfile,FollowerList=[],statusList=[]):

    reach,favorite_count, retweet_count = [], [],[]
    for line in FollowerList:
        profile = json.loads(line)
        reach.append((profile['screen_name'], profile['followers_count']))

    profile = json.loads(UserProfile)
    followersCount = profile['followers_count']
    tweetsCount = profile['statuses_count']
    sum_reach = sum([x[1] for x in reach])
    avg_followers = round(sum_reach / followersCount, 2)
    for line in statusList:
        tweet = json.loads(line)
        favorite_count.append(tweet['favorite_count'])
        retweet_count.append(tweet['retweet_count'])
    avg_favorite = round(sum(favorite_count) / tweetsCount, 2)
    avg_retweet = round(sum(retweet_count) / tweetsCount, 2)
    favorite_per_user = round(sum(favorite_count) / followersCount, 2)
    retweet_per_user = round(sum(retweet_count) / followersCount, 2)

    return followersCount,sum_reach,avg_followers,sum(favorite_count),avg_favorite,favorite_per_user,sum(retweet_count),avg_retweet,retweet_per_user


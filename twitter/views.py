from django.shortcuts import render
from . import authentication
from . import methods
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
from django.http import HttpResponse
from tweepy import Cursor
from collections import defaultdict

# Create your views here.

#(GET) View For Home Page
def index(request):

    context = {}
    return render(request, 'twitter/index.html', context)

#(POST) View For Analysis Page
def PostIndex(request):

    if (request.POST):
        Sname = request.POST['screenName']


    #Getting User Profile
    try:
        user_profile = methods.GetUserProfile(Sname)
    except Exception :
        context={'ErrorMessage': True }
        return render(request, 'twitter/index.html', context)
    UserProfile = json.loads(user_profile)
    UserName=UserProfile.get('name')
    UserLocation=UserProfile.get('location')
    UserDescription=UserProfile.get('description')
    UserCreatedAt=UserProfile.get('created_at')
    UserNoOfTweets=UserProfile.get('statuses_count')
    UserFavoritesCount=UserProfile.get('favourites_count')

    #Getting User TimeLine
    UserTimeLine = methods.GetUserTimeline(Sname)

    #Get Top 5 tweets from user timeline
    TweetList=methods.GetTopTweets(UserTimeLine)

    #Getting List of followers of user
    FollowerList=methods.GetFollowers(Sname)

    #Getting List of Freinds of user
    FreindList = methods.GetFreinds(Sname)

    #Getting Hashtags Analysis
    tweetsNoOfHashtags, tweetsNo_Of_Hashtags_with_percent, tweetsWithHashtags,\
    tweets_with_hashtags_percent, percentEliteList =methods.NoOfHashtags(UserTimeLine)

    #Getting the top 10 Hashtags
    HashtagList= methods.CalculatingHashtags(UserTimeLine)

    #Getting the top 10 most mentioned users
    UserMentionList=methods.GetUserMentions(UserTimeLine)

    #Gettint the top 10 most used words(terms)
    TermFrequencyList = methods.GetTermFrequency(UserTimeLine)

    #Getting the no. of freinds followers mutual freinds
    mutual_friends,followers_not_following,friends_not_following,FreindNames,FollowerNames=methods.FriendAndFollowerNames(FollowerList,FreindList)

    #Getting Influence And Engagement
    followersCount, sum_reach, avg_followers, favorite_count, avg_favorite, favorite_per_user, \
    retweet_count, avg_retweet, retweet_per_user = methods.InfluenceAndEngagement(user_profile,FollowerList,UserTimeLine)

    #Getting sentiment analysis
    list = methods.performAnalysis(UserTimeLine)

    context={'Sname':Sname,'UserName':UserName,'UserNoOfTweets':UserNoOfTweets,'UserFavoritesCount':UserFavoritesCount,'UserLocation':UserLocation,'UserDescription':UserDescription,'UserCreatedAt':UserCreatedAt,
            'tweetsNoOfHashtags':tweetsNoOfHashtags,'tweetsNo_Of_Hashtags_with_percent':tweetsNo_Of_Hashtags_with_percent,
            'tweetsWithHashtags':tweetsWithHashtags,'tweets_with_hashtags_percent':tweets_with_hashtags_percent,'percentEliteList':percentEliteList,'HashtagList':HashtagList,
            'UserMentionList': UserMentionList,'TermFrequencyList':TermFrequencyList,'followersCount':followersCount, 'sum_reach':sum_reach,'avg_followers':avg_followers,
            'favorite_count':favorite_count ,'avg_favorite':avg_favorite ,'favorite_per_user':favorite_per_user , 'retweet_count':retweet_count,
            'avg_retweet':avg_retweet,'retweet_per_user':retweet_per_user,'mutual_friends':mutual_friends, 'followers_not_following':followers_not_following, 'friends_not_following':friends_not_following,
            'FreindNames':FreindNames , 'FollowerNames':FollowerNames,'TweetList':TweetList,'SentimentList':list }
    return render(request, 'twitter/New.html', context)


#(GET) View For Creating Time Series
def TimeSeries(request):
    client = authentication.get_twitter_client()
    List = []
    all_dates = []
    userName = request.GET.get('userName') #request.GET['userName']
    #getting the user timeline
    for page in Cursor(client.user_timeline, screen_name=userName, count=200).pages(20):
        for status in page:
            List.append(json.dumps(status._json) + "\n")

    for line in List:
        tweet = json.loads(line)
        all_dates.append(tweet.get('created_at'))

    # get users profile
    profile = client.get_user(screen_name=userName)
    user_profile = (json.dumps(profile._json, indent=4))
    userProfile = json.loads(user_profile)

    idx = pd.DatetimeIndex(all_dates)
    ones = np.ones(len(all_dates))
    # the actual series (at series of 1s for the moment)
    my_series = pd.Series(ones, index=idx)

    # Resampling / bucketing into 1-minute buckets
    per_minute = my_series.resample('1M', how='sum').fillna(0)
    # Plotting the series
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_title("Tweet Frequencies")
    # hours = mdates.MinuteLocator(interval=20)
    hours = mdates.MonthLocator(interval=12)
    date_formatter = mdates.DateFormatter('%Y')
    datemin = (userProfile.get('created_at'))  # UserProfile['created_at']
    datemin = datetime.strptime(datemin, '%a %b %d %H:%M:%S %z %Y')
    datemax = str(datetime.today())
    datemax = datetime.strptime(datemax, '%Y-%m-%d %H:%M:%S.%f')
    # datemin = datetime(2018,1,1,1,1)
    # datemax = datetime(2019, 1, 1, 1, 1)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.set_xlim(datemin, datemax)
    max_freq = per_minute.max()
    ax.set_ylim(0, max_freq)
    ax.plot(per_minute.index, per_minute)
    # plt.savefig('tweet_time_series.png')

    buffer = io.BytesIO()
    buffer.seek(0)
    plt.savefig(buffer, format='png')

    return HttpResponse(buffer.getvalue(), content_type="Image/png")
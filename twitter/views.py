import base64

from django.shortcuts import render
from . import forms
from . import authentication
from . import methods
import json

from collections import defaultdict


import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import pickle
import io
from django.http import HttpResponse
from matplotlib import pylab
# Create your views here.



def index(request):

    hashtagList=[]
    #hashtags = Counter()
    FriendList=[]
    FollowerList=[]
    percentEliteList=[]
    reach1 = []

    favorite_count1, retweet_count1 = [], []
    hashtag_count = defaultdict(int)


    screen_name ='PacktPub'
    context = {}



    # context={'mutual_friends':len(mutual_friends), 'followers_not_following':len(followers_not_following),'friends_not_following':len(friends_not_following),
    #           'LengthOfFreinds':len(FreindNames),'LengthOfFollowers' : len(FollowerNames) , 'screen_name': screen_name }
    return render(request, 'twitter/index.html', context)


def PostIndex(request):

    if (request.POST):
        Sname = request.POST['screenName']

            


    context={'Sname':Sname}
    return render(request, 'twitter/New.html', context)
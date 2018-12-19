from tweepy import API
from tweepy import OAuthHandler


def get_twitter_auth():

  try:
      consumer_key = 'JWKTQCuMm0GAtXg6YYrGUJzx3'
      consumer_secret = 'D4PCqBeQQpCfi8V5M6BFoEX7XkpuU4ifNTwmNRLeSPilnfvK7C'
      access_token = '2823584030-EZV6sIfbSKuINaTtzI3E6Dn6JBrQItaW8DaYy9a'
      access_secret = 'qmFPe4jh5jb1mEZAdCiT72uOQZGbEhcTzjDozEFkOjKNj'
  except KeyError:
      print("TWITTER_* environment variables not set\n")
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  return auth

def get_twitter_client():
    auth=get_twitter_auth()
    client= API(auth)
    return client

def get_hashtags(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]

def NoOfHashtags (noOfTags , hashtagCount):
    percentEliteList = []
    tweetsWithHashtags= sum([count for noOfTags, count in hashtagCount.items() if noOfTags > 0])
    tweetsNoOfHashtags = hashtagCount[0]
    tweetsTotal = tweetsNoOfHashtags + tweetsWithHashtags
    tweets_with_hashtags_percent  = "%.2f" % (tweetsWithHashtags / tweetsTotal*100)
    tweetsNo_Of_Hashtags_with_percent = "%.2f" % (tweetsNoOfHashtags / tweetsTotal*100)

    print ("{} tweets without hashtags ({}%)".format(tweetsNoOfHashtags,tweetsNo_Of_Hashtags_with_percent))
    print("{} tweets with atleast one hashtag ({}%)".format(tweetsWithHashtags, tweets_with_hashtags_percent))
    # Dict = {'tweetsNoOfHashtags':tweetsNoOfHashtags,'tweetsNo_Of_Hashtags_with_percent':tweetsNo_Of_Hashtags_with_percent,
    #         'tweetsWithHashtags':tweetsWithHashtags, 'tweets_with_hashtags_percent':tweets_with_hashtags_percent,
    #         'hashtagCount':hashtagCount,'tweetsTotal':tweetsTotal }


    for tag_count, tweet_count in hashtagCount.items():
        if tag_count > 0:
            percent_total = "%.2f" % (tweet_count / tweetsTotal * 100)
            percent_elite = "%.2f" % (tweet_count / tweetsWithHashtags * 100)
            #print("{} tweets with {} hashtags ({}% total, {}% elite)".format(tweet_count, tag_count,percent_total,percent_elite))
            tempList=[tweet_count,tag_count,percent_total,percent_elite]
            percentEliteList.append(tempList)

    return (tweetsNoOfHashtags, tweetsNo_Of_Hashtags_with_percent, tweetsWithHashtags, tweets_with_hashtags_percent,percentEliteList)
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

from tweepy import API
from tweepy import OAuthHandler




def get_twitter_auth():

  try:
      #Credentials for the connection with twitter
      #please put your own credentials here
      consumer_key = ''
      consumer_secret = ''
      access_token = ''
      access_secret = ''
  except KeyError:
      print("TWITTER_* environment variables not set\n")
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  return auth

def get_twitter_client():
    auth=get_twitter_auth()
    client= API(auth)
    return client


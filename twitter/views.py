from django.shortcuts import render
from tweepy import Cursor
from . import authentication

# Create your views here.

def index(request):
    client = authentication.get_twitter_client()
    list=['0']

    for status in Cursor(client.home_timeline).items(10):
         list.append(status.text)
    context = {'status': list}
    return render(request, 'twitter/index.html', context)
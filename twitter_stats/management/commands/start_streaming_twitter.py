__author__ = 'zeemi'
from django.core.management.base import BaseCommand
from twitter_stats.models import Tweet
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_monitor_service.secrets import secrets


class Command(BaseCommand):
    help = 'Start monitor twitter streaming API. On data appearance Tweet object is pushed to db'

    def handle(self, *args, **options):
        tweets_count = len(Tweet.objects.all())
        self.stdout.write('Monitoring Twitter Stream API started! current number of tweets:"%s"' % tweets_count)
        twitter_streaming_task()


class TweetListener(StreamListener):
    def __init__(self):
        super(TweetListener, self).__init__()

    def on_data(self, data):
        try:
            user_name, user_screen_name = parse_tweet(data)
            print(data)
            # Tweet(user_name=user_name, user_screen_name=user_screen_name).save()
            print("increment stats for user:", user_name)
        except UnsupportedMessage:
            print("Message ignored: ", data)
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            #returning False in on_data disconnects the stream
            return False


class UnsupportedMessage(Exception):
    pass


def parse_tweet(raw_tweet):
    try:
        tweet = json.loads(raw_tweet)
        user_name = tweet['user']['name']
        user_screen_name = tweet['user']['screen_name']
        return user_name, user_screen_name
    except ValueError:
        raise UnsupportedMessage
    except TypeError:
        raise UnsupportedMessage

def twitter_streaming_task(filter=('golang')):
    l = TweetListener()
    auth = OAuthHandler(secrets['Consumer_Key'], secrets['Consumer_Secret'])
    auth.set_access_token(secrets['Access_Token'], secrets['Access_Token_Secret'])
    stream = Stream(auth, l)
    stream.filter(track=filter)

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from twitter_stats.models import Tweet
import django.test
import unittest
from twitter_stats.management.commands.start_streaming_twitter import parse_tweet, TweetListener, UnsupportedMessage


class TestTweetParser(unittest.TestCase):

    def test_parsing_valid_tweet(self):
        from twitter_stats.test.resources import raw_tweet

        user_name, user_screen_name = parse_tweet(raw_tweet)
        self.assertEqual(user_name, 'EDA')
        self.assertEqual(user_screen_name, 'cicilibirkiz')

    def test_heath_beat_tweet_should_be_ignored(self):
        from twitter_stats.test.resources import emtpy_tweet
        with self.assertRaises(UnsupportedMessage):
            parse_tweet(emtpy_tweet)

    def test_management_massages_should_be_ignored(self):
        from twitter_stats.test.resources import disconnect_msg
        with self.assertRaises(UnsupportedMessage):
            parse_tweet(disconnect_msg)


class TestTweetListener(django.test.TestCase):
    def test_tweet_should_be_saved_in_db_when_caught_by_twitter_stream_listener(self):
        from twitter_stats.test.resources import raw_tweet

        tweetl = TweetListener()
        tweet_no = len(Tweet.objects.all())
        self.assertEqual(tweet_no, 0)
        tweetl.on_data(raw_tweet)
        tweets = Tweet.objects.all()

        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0].user_name, 'EDA')
        self.assertEqual(tweets[0].user_screen_name, 'cicilibirkiz')



class TestStats(APITestCase):
    def test_tweets_statistics_per_user(self):
        import json
        Tweet(user_screen_name='user1', user_name='User 1').save()
        Tweet(user_screen_name='user1', user_name='User 1').save()
        Tweet(user_screen_name='user2', user_name='User 2').save()

        expected_json = '{"users":{"User 2":1,"User 1":2}}'
        url = reverse('user-stats')
        response = self.client.get(url)
        response.render()
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['users']["User 2"], 1)
        self.assertEqual(response_content['users']["User 1"], 2)




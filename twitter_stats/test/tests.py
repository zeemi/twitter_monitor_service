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
        self.assertEqual(user_name, 'Cayetano Benavent V.')
        self.assertEqual(user_screen_name, 'cayetanobv')

    def test_parsing_heathbeat_tweet(self):
        from twitter_stats.test.resources import emtpy_tweet
        with self.assertRaises(UnsupportedMessage):
            user_name, user_screen_name = parse_tweet(emtpy_tweet)


class TestTweetListener(django.test.TestCase):
    def test_tweet_creation(self):
        from twitter_stats.test.resources import raw_tweet
        #todo add test for tweed creation


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




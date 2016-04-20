from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from .models import Tweet


class TestStats(APITestCase):
    def test_tweets_statistics_per_user(self):
        Tweet(user_screen_name='user1', user_name='User 1').save()
        Tweet(user_screen_name='user1', user_name='User 1').save()
        Tweet(user_screen_name='user2', user_name='User 2').save()

        expected_json = '{"users":{"User 2":1,"User 1":2}}'
        url = reverse('user-stats')
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content.decode('utf-8'), expected_json)



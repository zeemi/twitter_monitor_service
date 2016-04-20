from django.db import models


class Tweet(models.Model):
    user_screen_name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    published_date = models.DateTimeField(blank=True, null=True)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import Tweet
from django.db.models import Count

class UserStatisticView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        users_stats = Tweet.objects.values('user_name').annotate(count=Count('user_name'))
        users_dict = {}
        for user_stats in users_stats:
            users_dict[user_stats["user_name"]]=user_stats['count']
        content = {'users': users_dict}
        return Response(content)


class TweetsCount(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        tweets_count = len(Tweet.objects.all())
        content = {'tweets': tweets_count}
        return Response(content)




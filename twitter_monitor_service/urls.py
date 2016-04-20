from django.conf.urls import include, url
from django.contrib import admin
from twitter_stats.views import TweetsCount, UserStatisticView
urlpatterns = [
    # Examples:
    # url(r'^$', 'twitter_monitor_service.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^twitter_stats/$', TweetsCount.as_view()),
    url(r'^twitter_stats/golang/$', UserStatisticView.as_view(), name='user-stats')
]

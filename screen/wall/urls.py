from django.conf.urls import patterns, url
from screen.wall.views import *

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', stream, name='event_stream'),
]

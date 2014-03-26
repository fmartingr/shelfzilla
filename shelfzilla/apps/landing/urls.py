from django.conf.urls import patterns, url

from .views import LandingView

urlpatterns = patterns(
    '',
    url(r'^landing/$', LandingView.as_view(), name='landing'),
)

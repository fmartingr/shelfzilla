# coding: utf-8

# django
from django.conf.urls import patterns, include, url

# app
from .views import BlockedView


# API
urlpatterns = patterns(
    '',
    # Manually blocked API endpoints
    url(r'^auth/register/', BlockedView.as_view()),
    # /auth
    url(r'^auth/', include('djoser.urls')),
    # /feed
    url(r'^', include('shelfzilla.apps.account.api.urls')),
)

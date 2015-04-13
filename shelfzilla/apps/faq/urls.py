# coding: utf-8

# django
from django.conf.urls import patterns, url

# app
from .views import FaqListView

urlpatterns = patterns(
    '',
    url(r'^$', FaqListView.as_view(), name='faq.list'),
)

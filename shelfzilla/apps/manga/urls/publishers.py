from django.conf.urls import patterns, url

from ..views.publishers import PublishersListView, PublishersDetailView

urlpatterns = patterns(
    '',
    url(r'^$', PublishersListView.as_view(), name='publishers.list'),
    url(
        r'^(?P<sid>\d+)/$',
        PublishersDetailView.as_view(),
        name='publishers.detail'),
    url(
        r'^(?P<sid>\d+)/(?P<slug>[\w-]+)/$',
        PublishersDetailView.as_view(),
        name='publishers.detail'),
)

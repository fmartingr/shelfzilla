from django.conf.urls import patterns, url

from ..views.series import SeriesListView, SeriesDetailView

urlpatterns = patterns(
    '',
    url(r'^$', SeriesListView.as_view(), name='series.list'),
    url(
        r'^(?P<sid>\d+)/$',
        SeriesDetailView.as_view(),
        name='series.detail'),
    url(
        r'^(?P<sid>\d+)/(?P<slug>[\w-]+)/$',
        SeriesDetailView.as_view(),
        name='series.detail'),
)

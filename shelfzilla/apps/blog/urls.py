from django.conf.urls import patterns, url

from .views import ListView, EntryView, SearchView, RSSView


urlpatterns = patterns(
    None,
    # Post list with page
    url(
        r'^page/(?P<page_number>\d+)/$',
        ListView.as_view(),
        name='list'
    ),
    # Post list
    url(
        r'^$',
        ListView.as_view(),
        name='list'
    ),
    # Single entry
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w\-]+)/$',
        EntryView.as_view(),
        name='item'
    ),
    # RSS
    url(
        r'^rss\.xml$',
        RSSView.as_view(),
        name='rss'
    ),
    # Search
    url(
        r'^search/$',
        SearchView.as_view(),
        name='search',
    )
)

from django.conf.urls import patterns, url

from ..views.search import SearchView

urlpatterns = patterns(
    '',
    url(r'^$', SearchView.as_view(), name='search'),
)

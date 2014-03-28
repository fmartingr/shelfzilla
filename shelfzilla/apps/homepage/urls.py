from django.conf.urls import patterns, url

from .views import HomepageView

urlpatterns = patterns(
    '',
    url(r'^$', HomepageView.as_view(), name='homepage'),
)

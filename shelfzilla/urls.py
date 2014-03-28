from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('shelfzilla.apps.landing.urls')),
    url(r'^', include('shelfzilla.apps.users.urls')),
    url(r'^series/', include('shelfzilla.apps.manga.urls.series')),
    url(r'^$', include('shelfzilla.apps.homepage.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

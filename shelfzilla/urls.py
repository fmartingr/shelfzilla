from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from .views import MessagesView

urlpatterns = patterns(
    '',
    url(r'^messages/$', MessagesView.as_view(), name="contrib.messages"),
    url(r'^', include('shelfzilla.apps.landing.urls')),
    url(r'^', include('shelfzilla.apps.users.urls')),
    url(r'^series/', include('shelfzilla.apps.manga.urls.series')),
    url(r'^$', include('shelfzilla.apps.homepage.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )

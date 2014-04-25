from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import MessagesView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^messages/$', MessagesView.as_view(), name="contrib.messages"),
    url(r'^', include('shelfzilla.apps.landing.urls')),
    url(r'^', include('shelfzilla.apps.users.urls')),
    url(r'^series/', include('shelfzilla.apps.manga.urls.series')),
    url(r'^volumes/', include('shelfzilla.apps.manga.urls.volumes')),
    url(r'^publishers/', include('shelfzilla.apps.manga.urls.publishers')),
    url(r'^$', include('shelfzilla.apps.homepage.urls')),
    url(r'^_admin/', include('shelfzilla.apps._admin.urls')),
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
        (
            r'^files/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.FILER_STORAGES['public']['main']['OPTIONS']['location']
            }
        ),
        (
            r'^files/thumbnails/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.FILER_STORAGES['public']['thumbnails']['OPTIONS']['location']
            }
        ),


    )

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            url(r'^rosetta/', include('rosetta.urls')),
        )

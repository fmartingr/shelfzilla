from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import MessagesView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^messages/$', MessagesView.as_view(), name="contrib.messages"),
    url(r'^$', include('shelfzilla.apps.homepage.urls')),
    url(r'^', include('shelfzilla.apps.landing.urls')),
    url(r'^', include('shelfzilla.apps.account.urls')),
    url(r'^blog/', include('shelfzilla.apps.blog.urls', namespace='blog')),
    url(r'^series/', include('shelfzilla.apps.manga.urls.series')),
    url(r'^volumes/', include('shelfzilla.apps.manga.urls.volumes')),
    url(r'^publishers/', include('shelfzilla.apps.manga.urls.publishers')),
    url(r'^search/', include('shelfzilla.apps.manga.urls.search')),
    url(r'^_admin/', include('shelfzilla.apps._admin.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^feedback/',
    #     include('object_feedback.urls', namespace="object_feedback")),
)

# API
urlpatterns += patterns(
    '',
    url(r'^api/v1/', include('shelfzilla.urls_api', namespace='api')),
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

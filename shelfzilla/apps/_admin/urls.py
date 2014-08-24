from django.conf.urls import patterns, url

from .views import VolumeChangeSeriesView, VolumeChangeCoverView

urlpatterns = patterns(
    '',
    url(r'^manga/volume/change_series/$',
        VolumeChangeSeriesView.as_view(),
        name="_admin.manga.volume.change_series"),
    url(r'^manga/volume/cover/(?P<volume_pk>\d+)/$',
        VolumeChangeCoverView.as_view(),
        name="_admin.manga.volume.cover"),
)

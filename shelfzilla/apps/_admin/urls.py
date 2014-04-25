from django.conf.urls import patterns, url

from .views import VolumeChangeSeriesView

urlpatterns = patterns(
    '',
    url(r'^manga/volume/change_series/$',
        VolumeChangeSeriesView.as_view(),
        name="_admin.manga.volume.change_series"),
)

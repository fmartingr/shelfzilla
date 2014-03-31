from django.conf.urls import patterns, url

from ..views.volumes import WishlistVolumeView, HaveVolumeView

urlpatterns = patterns(
    '',
    url(r'^(?P<vid>\d+)/wishlist_it/$',
        WishlistVolumeView.as_view(),
        name='volume.wishlist'),
    url(r'^(?P<vid>\d+)/have_it/$',
        HaveVolumeView.as_view(),
        name='volume.have_it'),
)

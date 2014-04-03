from django.conf.urls import patterns, url

from .views import LoginView, LogoutView, ProfileView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(
        r'^profile/$',
        ProfileView.as_view(),
        name="profile"),
    url(
        r'^profile/(?P<section>\w+)/$',
        ProfileView.as_view(),
        name="profile"),
)

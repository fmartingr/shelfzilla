from django.conf.urls import patterns, url

from .views import LoginView, LogoutView, UserProfileView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(
        r'^user/(?P<username>[\w\d\-\.]+)/$',
        UserProfileView.as_view(),
        name="profile"),
    url(
        r'^user/(?P<username>[\w\d\-\.]+)/(?P<section>\w+)/$',
        UserProfileView.as_view(),
        name="profile"),
)

# coding: utf-8

# third
from rest_framework.routers import DefaultRouter

# own
from .views import FeedViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'feed', FeedViewSet, base_name='feed')
urlpatterns = router.urls

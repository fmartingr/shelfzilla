# coding: utf-8

# third
from rest_framework.routers import DefaultRouter

# own
from .views import VolumesViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'volumes', VolumesViewSet)
router.register(r'publishers', VolumesViewSet)

urlpatterns = router.urls

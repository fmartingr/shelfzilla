# coding: utf-8

# third
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

# own
from .serializers import PublisherSerializer, VolumeSerializer
from ..models import Publisher, Volume


class PublishersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.filter(hidden=False)
    paginate_by = 20

    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class VolumesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = VolumeSerializer
    queryset = Volume.objects.filter(hidden=False)
    paginate_by = 20

    filter_fields = ('series', )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'number', 'series__name', )

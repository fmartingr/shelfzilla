# coding: utf-8

# python
from itertools import chain
import json

# third
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# own
from shelfzilla.apps.manga.models import (
    UserReadVolume, UserHaveVolume, UserWishlistVolume
)


class FeedViewSet(viewsets.ViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        owned_list = UserHaveVolume.objects.filter(user=request.user)
        wishlisted_list = UserWishlistVolume.objects.filter(user=request.user)
        read_list = UserReadVolume.objects.filter(user=request.user)

        timeline = sorted(
            chain(owned_list, wishlisted_list, read_list),
            key=lambda model: model.date,
            reverse=True
        )[:20]

        result = []
        for item in timeline:
            event = {
                'date': item.date,
                'message': item.timeline_message,
                'type': item.event_type,
            }
            result.append(event)

        return Response(result)

from datetime import datetime

from django.core.paginator import Paginator
from django.utils import translation
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Entry


class Config(object):
    entries_per_page = 10

config = Config()


def get_posts(query=None, limit=None):
    items = Entry.objects.filter(
        draft=False,
        date__lt=datetime.now()
    )
    if query and len(query) > 0:
        items = items.filter(
            Q(title__icontains=query) | \
            Q(content__icontains=query) | \
            Q(tags__name__iexact=query)
        ).distinct()

    items = items.order_by('-date')

    if limit:
        items = items[:limit]

    return items


def get_paginator(request, page_number=1, item=None, **kwargs):
    item_index = None
    page = None
    items = get_posts(query=kwargs.get('query', None))
    entries_per_page = config.entries_per_page
    paginator = Paginator(items, entries_per_page)
    if item:
        for index, obj in enumerate(items):
            if obj == item:
                item_index = index
                break
        if item_index:
            page_number = (item_index / entries_per_page) + 1

    if page_number:
        page = paginator.page(page_number)

    return paginator, page

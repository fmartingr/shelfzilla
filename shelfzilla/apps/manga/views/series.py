import string
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _

from shelfzilla.views import View
from ..models import Series


class SeriesView(View):
    section = 'series'


class SeriesListView(SeriesView):
    template = 'manga/series/list.html'
    filters = ['other']

    def get(self, request):
        letters = list(string.ascii_uppercase)
        current_letter = request.GET.get('letter', 'A')

        items = self.get_items(current_letter)

        context = {
            'items': items,
            'letters': letters,
            'current_letter': current_letter
        }
        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)

    def get_items(self, letter):
        result = Series.objects.all()
        if len(letter) == 1:
            result = Series.objects.filter(name__istartswith=letter)
        elif letter == 'all':
            result = Series.objects.all()
        elif letter == 'other':
            result = Series.objects.exclude(name__regex=r'^[a-zA-Z]')

        return result


class SeriesDetailView(SeriesView):
    template = 'manga/series/detail.html'

    def get(self, request, sid, slug=None):
        if slug:
            item = get_object_or_404(Series, pk=sid, slug=slug)
        else:
            item = get_object_or_404(Series, pk=sid)

        for pub in item.publishers:
            pub.series_volumes = pub.get_series_volumes(item)

        context = {
            'item': item,
            # 'publisher_volumes': publisher_volumes
        }

        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)

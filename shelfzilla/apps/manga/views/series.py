from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from shelfzilla.views import View
from ..models import Series


class SeriesView(View):
    section = 'series'


class SeriesListView(SeriesView):
    template = 'manga/series/list.html'

    def get(self, request):
        items = Series.objects.all()
        context = {
            'items': items
        }
        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)


class SeriesDetailView(SeriesView):
    template = 'manga/series/detail.html'

    def get(self, request, sid, slug=None):
        if slug:
            item = get_object_or_404(Series, pk=sid, slug=slug)
        else:
            item = get_object_or_404(Series, pk=sid)

        context = {
            'item': item
        }

        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)

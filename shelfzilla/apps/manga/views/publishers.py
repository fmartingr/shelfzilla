from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from shelfzilla.views import View
from ..models import Publisher


class PublishersView(View):
    section = 'publishers'


class PublishersListView(PublishersView):
    template = 'manga/publishers/list.html'

    def get(self, request):
        items = Publisher.objects.all()
        context = {
            'items': items
        }
        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)


class PublishersDetailView(PublishersView):
    template = 'manga/publishers/detail.html'

    def get(self, request, sid, slug=None):
        if slug:
            item = get_object_or_404(Publisher, pk=sid, slug=slug)
        else:
            item = get_object_or_404(Publisher, pk=sid)

        context = {
            'item': item
        }

        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)

from django.views.generic import View as DjangoView
from django.template import RequestContext
from django.shortcuts import render_to_response


class View(DjangoView):
    section = None

    def get_context(self, context):
        if self.section:
            context['navigation'] = {
                'section': self.section
            }

        return context


class MessagesView(View):
    template = 'contrib/messages.html'

    def get(self, request):
        ctx = RequestContext(request, {})
        return render_to_response(self.template, context_instance=ctx)

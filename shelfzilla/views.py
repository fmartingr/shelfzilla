import json
from django.views.generic import View as DjangoView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib import messages


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
    formats = ['html', 'json']

    def get(self, request):
        format = 'html'
        if 'format' in request.GET and request.GET['format'] in self.formats:
            format = request.GET['format']

        if format == 'html':
            ctx = RequestContext(request, {})
            result = render_to_response(self.template, context_instance=ctx)
        elif format == 'json':
            messages_json = []
            for message in messages.get_messages(request):
                messages_json.append(
                    {
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    }
                )
            result = HttpResponse(
                json.dumps(messages_json),
                content_type='application/json'
            )

        return result

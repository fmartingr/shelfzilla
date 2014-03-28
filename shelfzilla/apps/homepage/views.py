from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response


class HomepageView(View):
    template = 'homepage/home.html'

    def get(self, request):
        ctx = RequestContext(request, {})
        return render_to_response(self.template, context_instance=ctx)

from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response


class LoginView(View):
    template = 'landing/landing.html'

    def get(self, request):
        ctx = RequestContext(request, {})
        return render_to_response(self.template, context_instance=ctx)

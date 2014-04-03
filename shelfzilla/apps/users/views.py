from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import login

from .forms import LoginForm
from .models import User


class LoginView(View):
    template = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        context = {
            'login_form': LoginForm()
        }

        ctx = RequestContext(request, context)
        return render_to_response(self.template, context_instance=ctx)

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = login_form.authenticate()
            login(request, user)

            messages.success(
                request,
                _('Logged in successfully.')
            )

            return HttpResponseRedirect('/')

        context = {
            'login_form': login_form,
        }

        ctx = RequestContext(request, context)
        return render_to_response(self.template, context_instance=ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)

        messages.success(
            request,
            _('Logged out successfully')
        )

        return HttpResponseRedirect('/')


class ProfileView(View):
    template = 'users/profile/{}.html'

    def get(self, request, section='summary'):
        if request.user.is_authenticated():
            data = {
                'item': User.objects.get(pk=request.user.pk)
            }

            template = self.template.format(section)
            data = self.get_context_from_section(request, section, data)

            ctx = RequestContext(request, data)
            return render_to_response(template, context_instance=ctx)
        else:
            raise Http404

    def get_summary(self, request, context):
        context['SUMMARY'] = 'Y'
        return context

    def get_context_from_section(self, request, section, context):
        method = getattr(self, 'get_{}'.format(section), None)

        if method:
            context = method(request, context)

        return context

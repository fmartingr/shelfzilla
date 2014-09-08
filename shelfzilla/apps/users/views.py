from itertools import chain
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import login

from .forms import LoginForm
from .models import User
from shelfzilla.apps.manga.models import (
    UserReadVolume, UserHaveVolume, UserWishlistVolume
)


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


class UserProfileView(View):
    tempalte = 'users/profile.html'
    template_section = 'users/profile/{}.html'

    def get(self, request, username, section='summary'):
        user = get_object_or_404(User, username=username)
        data = {
            'item': user,
            'section': section
        }
        if section != 'summary':
            template = self.template_section.format(section)
        else:
            template = self.tempalte
        data = self.get_context_from_section(request, section, data, user)

        ctx = RequestContext(request, data)
        return render_to_response(template, context_instance=ctx)

    def get_summary(self, request, context, user):
        owned_list = UserHaveVolume.objects.filter(user=user)
        wishlisted_list = UserWishlistVolume.objects.filter(user=user)
        read_list = UserReadVolume.objects.filter(user=user)

        timeline = sorted(
            chain(owned_list, wishlisted_list, read_list),
            key=lambda model: model.date,
            reverse=True
        )[:20]
        context['timeline'] = timeline
        return context

    def get_context_from_section(self, request, section, context, user):
        method = getattr(self, 'get_{}'.format(section), None)

        if method:
            context = method(request, context, user)

        return context

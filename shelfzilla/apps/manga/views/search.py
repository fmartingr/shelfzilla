from django.template import RequestContext
from django import forms
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404

from shelfzilla.views import View
from ..models import Series


class SearchForm(forms.Form):
    q = forms.CharField(max_length=64, label=_('Search'),
                        widget=forms.TextInput(
                            attrs={'placeholder': _('Search')})
    )


class SearchView(View):
    template = 'manga/search.html'
    section = 'search'

    def post(self, request):
        search_query = ''
        items = []
        form = SearchForm(request.POST)

        if form.is_valid():
            search_query = form.cleaned_data['q']

            items = Series.objects.filter(name__icontains=search_query)

        context = {
            'items': items,
            'search_query': search_query
        }
        ctx = RequestContext(request, self.get_context(context))
        return render_to_response(self.template, context_instance=ctx)

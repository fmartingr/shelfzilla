from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from shelfzilla.views import View
import utils as blog_utils
from .models import Entry


class ListView(View):
    section = 'blog'
    template = 'blog/list.html'

    def get(self, request, page_number=1):
        if 'page' in request.GET:
            page_number = int(request.GET['page'])

        paginator, page = blog_utils.get_paginator(request, page_number)

        context = {}

        context['page'] = page
        context['page_number'] = page_number
        context['paginator'] = paginator

        context = RequestContext(request, context)
        return render_to_response(self.template, context_instance=context)


class EntryView(View):
    section = 'blog'
    template = 'blog/entry.jinja'

    def get(self, request, year, month, day, slug):
        try:
            filters = {
                'slug': slug,
                'date__year': int(year),
                'date__month': int(month),
                'date__day': int(day),
            }

            item = Entry.objects.get(**filters)
        except Entry.DoesNotExist:
            raise Http404

        paginator, page = blog_utils.get_paginator(request, item=item)

        context = {}
        context['page'] = page
        context['paginator'] = paginator
        context['item'] = item

        context = RequestContext(request, context)
        return render_to_response(self.template, context_instance=context)


class SearchView(ListView):
    template = 'blog/search.jinja'

    def post(self, request):
        page_number = 1
        if 'page' in request.GET:
            page_number = int(request.GET['page'])

        search_query = request.POST['query']

        if not search_query:
            return HttpResponseRedirect(reverse('blog:list'))

        paginator, page = blog_utils.get_paginator(
            request, page_number, query=search_query
        )

        context = {}
        context['page'] = page
        context['page_number'] = page_number
        context['paginator'] = paginator
        context['search_query'] = search_query

        context = RequestContext(request, context)
        return render_to_response(self.template, context_instance=context)


class RSSView(View):
    template = 'blog/rss.jinja'

    def get(self, request):
        limit = 20
        items = blog_utils.get_posts(limit=limit)
        context = {}
        context['items'] = items

        context = RequestContext(request, context)
        return render_to_response(
            'blog/rss.jinja',
            context_instance=context,
            mimetype='text/xml'
        )

# coding: utf-8

# django
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from django.contrib.auth import get_user_model

# shelfzilla.faq
from .models import QuestionAnswerCategory


class FaqListView(View):
    template = 'faq/list.html'

    def get(self, request):
        data = {
            'categories': QuestionAnswerCategory.objects.all(),
            'navigation': {
                'section': 'faqs',
            },
        }

        ctx = RequestContext(request, data)
        return render_to_response(self.template, context_instance=ctx)

# coding: utf-8

# django
from django.contrib import admin

# app
from .models import Question, TranslatedQuestion


class TranslatedQuestionInline(admin.TabularInline):
    model = TranslatedQuestion

class QuestionAdmin(admin.ModelAdmin):
    inlines = (TranslatedQuestionInline, )


admin.site.register(Question, QuestionAdmin)

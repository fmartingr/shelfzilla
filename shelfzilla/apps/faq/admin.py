# coding: utf-8

# django
from django.contrib import admin

# app
from .models import QuestionAnswerCategory, QuestionAnswer


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer

class QuestionAnswerCategoryAdmin(admin.ModelAdmin):
    inlines = (QuestionAnswerInline, )


admin.site.register(QuestionAnswerCategory, QuestionAnswerCategoryAdmin)

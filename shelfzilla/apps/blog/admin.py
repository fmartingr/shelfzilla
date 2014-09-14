from django.contrib import admin
from .models import Entry, Tag
from django import forms
from django.utils.translation import ugettext as _
from django import forms
from django.db import models
from ckeditor.widgets import CKEditorWidget
import reversion


#
#   ENTRY
#
class EntryAdmin(reversion.VersionAdmin):
    list_display = ('title', 'date', 'status', 'tag_list', 'preview_link')
    list_display_links = ('title', )

    list_filter = ('date', 'draft', )
    search_fields = ('title', 'content', )

    prepopulated_fields = {"slug": ("title",)}

    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content')),
    )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('title', 'slug', 'draft', 'date', 'tags', )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-content full-width',),
            'fields': ('content', )
        }),
    ]

    def preview_link(self, obj):
        return '<a href="%s">View &raquo;</a>' % (
            obj.get_absolute_url()
        )
    preview_link.allow_tags = True

    def tag_list(self, obj):
        return ", ".join([x.name for x in obj.tags.all()])

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super(self.__class__, self).save_model(request, obj, form, change)

    class Media:
        #css = {
        #    "all": ("ckeditor/redactor.css",)
        #}
        # js = (
        #     "ckeditor/ckeditor.js",
        #     "js/wysiwyg.js",
        # )
        pass

admin.site.register(Entry, EntryAdmin)


#
#   TAG
#
class TagAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Tag, TagAdmin)

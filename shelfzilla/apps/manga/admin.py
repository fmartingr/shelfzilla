from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import reversion


from .models import Publisher, Series, Volume, Person


###
# IMPORT EXPORT RESOURCES
###
class PublisherResource(resources.ModelResource):
    class Meta:
        model = Publisher


class SeriesResource(resources.ModelResource):
    class Meta:
        model = Series


class VolumeResource(resources.ModelResource):
    class Meta:
        model = Volume


class PersonResource(resources.ModelResource):
    class Meta:
        model = Person


# Actions
def mark_for_review(self, request, queryset):
    queryset.update(for_review=True)
    messages.success(request, _('Items marked for review'))


def unmark_for_review(self, request, queryset):
    queryset.update(for_review=False)
    messages.success(request, _('Items unmarked for review'))


# Modeladmin
class PublisherAdmin(ImportExportModelAdmin, reversion.VersionAdmin):
    resource_class = PublisherResource
    list_display = ['name', 'series_count']
    prepopulated_fields = {"slug": ("name",)}
    actions = (mark_for_review, unmark_for_review, )

    suit_form_tabs = (
        ('general', _('General')),
        ('review', _('Review')),
        ('advanced', _('Advanced')),
    )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'slug', 'url')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-review',),
            'fields': ('for_review', 'for_review_comment')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-advanced',),
            'fields': ('hidden', )
        }),
    ]

    def series_count(self, obj):
        return obj.series.count()
    series_count.short_description = _('Series')

admin.site.register(Publisher, PublisherAdmin)


class SeriesAdmin(ImportExportModelAdmin, reversion.VersionAdmin):
    resource_class = SeriesResource
    list_display = ['name', 'volumes_count']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', )
    search_filters = ('hidden', )
    actions = (mark_for_review, unmark_for_review, )

    suit_form_tabs = (
        ('general', _('General')),
        ('volumes', _('Volumes')),
        ('review', _('Review')),
        ('advanced', _('Advanced')),
    )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'slug', 'cover', 'summary', 'finished',
                       'original_publisher', 'art', 'story', )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-review',),
            'fields': ('for_review', 'for_review_comment')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-advanced',),
            'fields': ('hidden', 'folder')
        }),
    ]

    suit_form_includes = (
        ('_admin/manga/series/includes/volumes.html', 'top', 'volumes'),
    )

    def volumes_count(self, obj):
        return obj.volumes.count()
    volumes_count.short_description = _('Volumes')

admin.site.register(Series, SeriesAdmin)


class VolumeAdmin(ImportExportModelAdmin, reversion.VersionAdmin):
    resource_class = VolumeResource
    # list_display_links = ('number', )
    list_display = ('series', 'publisher', 'number', 'name', 'release_date',)
    search_fields = ('number', 'series__name', )
    list_filter = ('series', 'for_review', )
    # list_editable = ('series', )
    actions = ('change_series', mark_for_review, unmark_for_review, )

    suit_form_tabs = (
        ('general', _('General')),
        ('review', _('Review')),
        ('advanced', _('Advanced')),
    )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('series', 'publisher', 'number', 'name', 'cover',
                       'isbn_10', 'isbn_13', 'retail_price', 'pages',
                       'release_date', )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-review',),
            'fields': ('for_review', 'for_review_comment')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-advanced',),
            'fields': ('hidden', )
        }),
    ]

    def change_series(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(
            "{}{}".format(
                reverse('_admin.manga.volume.change_series'),
                "?volumes={}".format(",".join(selected))
            )
        )
    change_series.short_description = _('Change volume series')

admin.site.register(Volume, VolumeAdmin)


class PersonAdmin(ImportExportModelAdmin, reversion.VersionAdmin):
    resource_class = PersonResource
    suit_form_tabs = (
        ('general', _('General')),
        ('review', _('Review')),
        ('advanced', _('Advanced')),
    )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-review',),
            'fields': ('for_review', 'for_review_comment')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-advanced',),
            'fields': ('hidden', )
        }),
    ]

admin.site.register(Person, PersonAdmin)

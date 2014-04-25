from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
import reversion
from .models import Publisher, Series, Volume, Person


class PublisherAdmin(reversion.VersionAdmin):
    list_display = ['name', 'series_count']
    prepopulated_fields = {"slug": ("name",)}

    def series_count(self, obj):
        return obj.series.count()
    series_count.short_description = _('Series')

admin.site.register(Publisher, PublisherAdmin)


class SeriesAdmin(reversion.VersionAdmin):
    list_display = ['name', 'volumes_count']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', )
    search_filters = ('hidden', )

    def volumes_count(self, obj):
        return obj.volumes.count()
    volumes_count.short_description = _('Volumes')

admin.site.register(Series, SeriesAdmin)


class VolumeAdmin(reversion.VersionAdmin):
    # list_display_links = ('number', )
    list_display = ('series', 'publisher', 'number', 'name', 'release_date',)
    search_fields = ('number', 'series__name', )
    list_filter = ('series', 'for_review', )
    # list_editable = ('series', )
    actions = ['change_series']

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


class PersonAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Person, PersonAdmin)

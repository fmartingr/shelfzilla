from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
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
        return obj.volumes.distinct('number').count()
    volumes_count.short_description = _('Volumes')


admin.site.register(Series, SeriesAdmin)


class VolumeAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Volume, VolumeAdmin)


class PersonAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Person, PersonAdmin)

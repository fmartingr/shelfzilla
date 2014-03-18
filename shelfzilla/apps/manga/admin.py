from django.contrib import admin
import reversion
from .models import Publisher, Series, Volume


class PublisherAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Publisher, PublisherAdmin)


class SeriesAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Series, SeriesAdmin)


class VolumeAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Volume, VolumeAdmin)

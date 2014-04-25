from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from filer.fields.image import FilerImageField
from filer.models.foldermodels import Folder

from shelfzilla.models import Model


class Publisher(Model):
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    url = models.URLField(_('URL'), blank=True, null=True)

    # Cache
    _series = None
    _volumes = None

    def __unicode__(self):
        return u'{}'.format(self.name)

    def get_series_volumes(self, series):
        try:
            series = self.series.get(pk=series.pk)
            return series.volumes.filter(publisher=self)
        except Series.DoesNotExist:
            return []

    @property
    def series(self):
        result = []
        if not self._series:
            queryset = self.volumes.order_by('series__id')\
                .distinct('series').values_list('series')

            result = Series.objects.filter(pk__in=queryset)

            self._series = result
        return self._series

    class Meta:
        ordering = ['name']
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')


class Series(Model):
    name = models.CharField(_('Name'), max_length=256)
    slug = models.SlugField(_('Slug'), blank=True, null=True, max_length=256)
    cover = FilerImageField(blank=True, null=True)
    summary = models.TextField(_('Summary'), blank=True, null=True)
    finished = models.BooleanField(_('Finished'), default=False)

    original_publisher = models.ForeignKey(
        Publisher, related_name='original_series', null=True)

    art = models.ManyToManyField(
        'Person', related_name='artist_of', null=True)
    story = models.ManyToManyField(
        'Person', related_name='scriptwriter_of', null=True)

    folder = models.ForeignKey(Folder, null=True, blank=True)

    # Cache
    _publishers = None

    def __unicode__(self):
        return u'{}'.format(self.name)

    def have_review_pending(self):
        if self.for_review:
            return True

        for vol in self.volumes.all():
            if vol.for_review:
                return True

        return False

    @property
    def volumes_by_publisher(self):
        return self.volumes.order_by('publisher__name', 'number')

    @property
    def last_volume_cover(self):
        return self.volumes.filter(cover__isnull=False).last().cover

    @property
    def publishers(self):
        if not self._publishers:
            result = []
            queryset = self.volumes.order_by('publisher__id')\
                .distinct('publisher').values_list('publisher')
            result = Publisher.objects.filter(pk__in=queryset)

            self._publishers = result

        return self._publishers

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Series')


class Volume(Model):
    number = models.IntegerField(_('Number'), null=True, blank=True)
    name = models.CharField(_('Name'), max_length=64, null=True, blank=True)
    series = models.ForeignKey(Series, related_name="volumes")
    publisher = models.ForeignKey(Publisher, related_name="volumes")
    cover = FilerImageField(null=True, blank=True)
    isbn_10 = models.CharField(
        _('ISBN-10'), max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(
        _('ISBN-13'), max_length=13, blank=True, null=True)

    retail_price = models.DecimalField(
        _('Retail price'), max_digits=5, decimal_places=2,
        null=True, blank=True)
    pages = models.IntegerField(_('Pages'), null=True, blank=True)
    release_date = models.DateField(_('Release date'), null=True)

    def __unicode__(self):
        return u'{} #{}'.format(self.series.name, self.number)

    class Meta:
        ordering = ['series__name', 'number']
        verbose_name = _('Volume')
        verbose_name_plural = _('Volumes')


class Person(Model):
    name = models.CharField(_('Name'), max_length=256)
    slug = models.SlugField(_('Slug'), blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


#
# RELATIONS
#
class UserHaveVolume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='have_volumes')
    volume = models.ForeignKey(Volume, related_name='owned_by')

    def __unicode__(self):
        return "{} {} {}".format(
            self.user.username,
            _('have'),
            self.volume
        )


class UserWishlistVolume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='wishlisted_volumes')
    volume = models.ForeignKey(Volume, related_name='wishlisted_by')

    def __unicode__(self):
        return "{} {} {}".format(
            self.user.username,
            _('wants'),
            self.volume
        )

#
# SIGNALS
#
def series_check_filer(sender, instance, created, **kwargs):
    name = instance.name

    # Check folder
    if not instance.folder:
        folder, is_new = Folder.objects.get_or_create(
            name=name,
            parent_id=settings.COVER_FOLDER_PK,
            owner_id=settings.COVER_FOLDER_OWNER_PK,
        )
        instance.folder = folder
        instance.save()
    else:
        # Check for name change
        if instance.folder.name != name:
            instance.folder.name = name
            instance.folder.save()

    # Check file name
    if instance.cover:
        if instance.cover.name != 'Cover':
            instance.cover.name = 'Cover'
            instance.cover.save()

        if instance.cover.folder != instance.folder:
            instance.cover.folder = instance.folder
            instance.cover.save()


def volume_check_filer(sender, instance, created, **kwargs):
    if instance.cover:
        # Check cover to be in series folder
        if instance.cover.folder != instance.series.folder:
            instance.cover.folder = instance.series.folder
            instance.cover.save()

        # Check filename
        if instance.name:
            cover_name = slugify(instance.name)
        elif instance.number:
            cover_name = '{:03}'.format(instance.number)
        if instance.cover.name != cover_name:
            instance.cover.name = cover_name
            instance.cover.save()


def series_delete_folder(sender, instance, using, **kwargs):
    if instance.folder:
        instance.folder.delete()


def volume_delete_cover(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete()

post_save.connect(series_check_filer, sender=Series)
post_save.connect(volume_check_filer, sender=Volume)
post_delete.connect(series_delete_folder, sender=Series)
post_delete.connect(volume_delete_cover, sender=Volume)

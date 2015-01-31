from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.core.urlresolvers import reverse
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

    def get_absolute_url(self):
        args = [self.pk]
        if self.slug:
            args.append(self.slug)
        return reverse('publishers.detail', args=args)

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
    SERIES_STATUS = (
        ('open', _('Open')),
        ('finished', _('Finished')),
        ('cancelled', _('Cancelled')),
        ('on-hold', _('On-hold'))
    )

    name = models.CharField(_('Name'), max_length=256)
    slug = models.SlugField(_('Slug'), blank=True, null=True, max_length=256)
    cover = FilerImageField(blank=True, null=True)
    summary = models.TextField(_('Summary'), blank=True, null=True)
    finished = models.BooleanField(_('Finished'), default=False)
    status = models.CharField(_('Status'), choices=SERIES_STATUS,
                              default='open', max_length=16)

    original_publisher = models.ForeignKey(
        Publisher, related_name='original_series', null=True, blank=True)

    art = models.ManyToManyField(
        'Person', related_name='artist_of', null=True, blank=True)
    story = models.ManyToManyField(
        'Person', related_name='scriptwriter_of', null=True, blank=True)

    folder = models.ForeignKey(Folder, null=True, blank=True)

    # Cache
    _languages = None

    def __unicode__(self):
        return u'{}'.format(self.name)

    def have_review_pending(self):
        if self.for_review:
            return True

        for vol in self.volumes.all():
            if vol.for_review:
                return True

        return False

    def get_absolute_url(self):
        args = [self.pk]
        if self.slug:
            args.append(self.slug)
        return reverse('series.detail', args=args)

    def get_status_display_class(self):
        pairs = {
            'open': 'success', 'finished': 'success', 'cancelled': 'danger',
            'on-hold': 'warning'
        }

        return pairs[self.status]

    @property
    def volumes_by_publisher(self):
        return self.volumes.order_by('publisher__name', 'language', 'number')

    @property
    def last_volume_cover(self):
        return self.volumes.filter(cover__isnull=False).last().cover

    def languages(self):
        if not self._languages:
            result = []
            queryset = self.volumes.order_by('language__id')\
                .distinct('language').values_list('language')
            result = Language.objects.filter(pk__in=queryset)

            self._languages = result

        return self._languages

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Series')


class SeriesSummary(Model):
    series = models.ForeignKey('Series', related_name='summaries')
    language = models.ForeignKey('Language')
    summary = models.TextField(_('Summary'), null=True, blank=True)

    class Meta:
        unique_together = ('series', 'language', )


class SeriesPublisher(Model):
    series = models.ForeignKey('Series', related_name='publishers')
    publisher = models.ForeignKey('Publisher', related_name='series_published')
    status = models.CharField(_('Status'), choices=Series.SERIES_STATUS,
                              default='open', max_length=16)
    actual_publisher = models.BooleanField(_('Current publisher'),
                                            default=True)

    def get_status_display_class(self):
        pairs = {
            'open': 'success', 'finished': 'success', 'cancelled': 'danger',
            'on-hold': 'warning'
        }

        return pairs[self.status]

    @property
    def volumes(self):
        return self.series.volumes.filter(publisher=self.publisher)


class Volume(Model):
    collection = models.ForeignKey('VolumeCollection', null=True,
        related_name='volumes')
    number = models.IntegerField(_('Number'), null=True, blank=True)
    name = models.CharField(_('Name'), max_length=64, null=True, blank=True)
    series = models.ForeignKey(Series, related_name="volumes")
    publisher = models.ForeignKey(Publisher, related_name="volumes")
    cover = FilerImageField(null=True, blank=True)
    isbn_10 = models.CharField(
        _('ISBN-10'), max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(
        _('ISBN-13'), max_length=13, blank=True, null=True)

    language = models.ForeignKey('Language', null=True)

    retail_price = models.DecimalField(
        _('Retail price'), max_digits=5, decimal_places=2,
        null=True, blank=True)
    pages = models.IntegerField(_('Pages'), null=True, blank=True)
    release_date = models.DateField(_('Release date'), null=True)

    def __unicode__(self):
        if self.name:
            return u'{} {}'.format(self.series.name, self.name)
        elif self.number:
            return u'{} #{}'.format(self.series.name, self.number)
        else:
            return u'{}'.format(self.series.name)

    class Meta:
        ordering = ['series__name', 'language', 'number']
        verbose_name = _('Volume')
        verbose_name_plural = _('Volumes')


class VolumeCollection(Model):
    name = models.CharField(_('Name'), max_length=32)
    series = models.ForeignKey('Series', related_name='collections')
    default = models.BooleanField(_('Default'), default=True)

    def __unicode__(self):
        return u'{} - {}'.format(self.series, self.name)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')


class Person(Model):
    name = models.CharField(_('Name'), max_length=256)
    slug = models.SlugField(_('Slug'), blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Language(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    code = models.CharField(_('Code'), max_length=5)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


#
# RELATIONS
#
class UserHaveVolume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='have_volumes')
    volume = models.ForeignKey(Volume, related_name='owned_by')
    date = models.DateTimeField(_('Date'), auto_now_add=True)

    _timeline_message = _('%(volume)s added to collection')
    _event_type = 'have'

    @property
    def event_type(self):
        return self._event_type

    @property
    def timeline_message(self):
        return self._timeline_message % {'volume': self.volume}

    def __unicode__(self):
        return "{} {} {}".format(
            self.user.username,
            _('have'),
            self.volume
        )

    class Meta:
        ordering = ('volume__series__name', 'volume__number', )


class UserWishlistVolume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='wishlisted_volumes')
    volume = models.ForeignKey(Volume, related_name='wishlisted_by')
    date = models.DateTimeField(_('Date'), auto_now_add=True)

    _timeline_message = _('%(volume)s wishlisted')
    _event_type = 'wishlist'

    @property
    def event_type(self):
        return self._event_type

    @property
    def timeline_message(self):
        return self._timeline_message % {'volume': self.volume}

    def __unicode__(self):
        return "{} {} {}".format(
            self.user.username.encode('utf-8'),
            _('wants'),
            self.volume.encode('utf-8'),
        )

    class Meta:
        ordering = ('volume__series__name', 'volume__number', )


class UserReadVolume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='read_volumes')
    volume = models.ForeignKey(Volume, related_name='read_by')
    date = models.DateTimeField(_('Date'), auto_now_add=True)

    _timeline_message = _('%(volume)s marked as read')
    _event_type = 'read'

    @property
    def event_type(self):
        return self._event_type

    @property
    def timeline_message(self):
        return self._timeline_message % {'volume': self.volume}

    def __unicode__(self):
        return "{} {} {}".format(
            self.user.username.encode('utf-8'),
            _('have read'),
            self.volume.encode('utf-8'),
        )

    class Meta:
        ordering = ('volume__series__name', 'volume__number', )


#
# SIGNALS
#
def series_check_filer(sender, instance, created, **kwargs):
    name = instance.name

    # Check folder
    # Fix for loaddata import
    if instance.folder_id:
        try:
            Folder.objects.get(pk=instance.folder_id)
        except Folder.DoesNotExist:
            instance.folder_id = None
            instance.folder = None

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
        cover_name = uuid4()
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
    try:
        if instance.cover:
            instance.cover.delete()
    except:
        pass

post_save.connect(series_check_filer, sender=Series)
post_save.connect(volume_check_filer, sender=Volume)
post_delete.connect(series_delete_folder, sender=Series)
post_delete.connect(volume_delete_cover, sender=Volume)

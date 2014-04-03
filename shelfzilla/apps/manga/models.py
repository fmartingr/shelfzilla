from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from filer.fields.image import FilerImageField
from filer.models.foldermodels import Folder

from shelfzilla.models import ReviewModel


class Publisher(ReviewModel):
    name = models.CharField(_('Name'), max_length=40)
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    url = models.URLField(_('URL'), blank=True, null=True)

    # Cache
    _series = None
    _volumes = None

    def __unicode__(self):
        return u'{}'.format(self.name)

    @property
    def series(self):
        result = []
        if not self._series:
            queryset = self.volumes.order_by('series__id')\
                .distinct('series').values_list('series')

            if queryset:
                result = Series.objects.filter(pk__in=queryset)

            self._series = result
        return self._series

    class Meta:
        ordering = ['name']
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')


class Series(ReviewModel):
    name = models.CharField(_('Name'), max_length=40)
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    cover = FilerImageField(blank=True, null=True)
    summary = models.TextField(_('Summary'), blank=True, null=True)
    finished = models.BooleanField(_('Finished'), default=False)

    folder = models.ForeignKey(Folder, null=True, blank=True)

    # Cache
    _publishers = None

    def __unicode__(self):
        return u'{}'.format(self.name)

    @property
    def publishers(self):
        if not self._publishers:
            result = []
            queryset = self.volumes.order_by('publisher__id')\
                .distinct('publisher').values_list('publisher')
            if queryset:
                result = Publisher.objects.filter(pk__in=queryset)

            self._publishers = result

        return self._publishers

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Series')


class Volume(ReviewModel):
    number = models.IntegerField(_('Number'))
    series = models.ForeignKey(Series, related_name="volumes")
    publisher = models.ForeignKey(Publisher, related_name="volumes")
    cover = FilerImageField(null=True, blank=True)
    isbn_10 = models.CharField(
        _('ISBN-10'), max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(
        _('ISBN-13'), max_length=13, blank=True, null=True)

    def __unicode__(self):
        return u'{} #{}'.format(self.series.name, self.number)

    class Meta:
        ordering = ['series__name', 'number']
        verbose_name = _('Volume')
        verbose_name_plural = _('Volumes')


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


# Signals
def series_check_filer(sender, instance, created, **kwargs):
    field = 'folder'
    name = instance.name

    # Check folder
    if not instance.folder:
        folder = Folder(
            name=name,
            parent_id=settings.COVER_FOLDER_PK,
            owner_id=settings.COVER_FOLDER_OWNER_PK,
        )
        folder.save()
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
        cover_name = '{:03}'.format(instance.number)
        if instance.cover.name != cover_name:
            instance.cover.name = cover_name
            instance.cover.save()


post_save.connect(series_check_filer, sender=Series)
post_save.connect(volume_check_filer, sender=Volume)
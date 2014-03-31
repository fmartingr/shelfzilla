from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from filer.fields.image import FilerImageField

from shelfzilla.models import ReviewModel


class Publisher(ReviewModel):
    name = models.CharField(_('Name'), max_length=40)
    url = models.URLField(_('URL'), blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.name)

    @property
    def series(self):
        return self.volumes.distinct('series')

    class Meta:
        ordering = ['name']
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')


class Series(ReviewModel):
    name = models.CharField(_('Name'), max_length=40)
    cover = FilerImageField(blank=True, null=True)
    summary = models.TextField(_('Summary'), blank=True, null=True)
    finished = models.BooleanField(_('Finished'), default=False)

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
            self.user.name,
            _('have'),
            self.volume
        )


class UserWishlistVolume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='wishlisted_volumes')
    volume = models.ForeignKey(Volume, related_name='wishlisted_by')

    def __unicode__(self):
        return "{} {} {}".format(
            self.user.name,
            _('wants'),
            self.volume
        )

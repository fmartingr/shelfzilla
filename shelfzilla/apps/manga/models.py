from django.db import models
from django.utils.translation import ugettext_lazy as _

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

    def __unicode__(self):
        return u'{}'.format(self.name)

    @property
    def publishers(self):
        return self.volumes.distinct('publisher')

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Series')


class Volume(ReviewModel):
    number = models.IntegerField(_('Number'))
    series = models.ForeignKey(Series, related_name="volumes")
    publisher = models.ForeignKey(Publisher, related_name="volumes")
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

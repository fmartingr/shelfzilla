from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, null=True, blank=True)
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return _("Site Configuration")

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configuration")


class SocialConfiguration(SingletonModel):
    twitter_account = models.CharField(max_length=64, blank=True, null=True)
    google_analytics = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return _("Social Configuration")

    class Meta:
        verbose_name = _("Social Configuration")
        verbose_name_plural = _("Social Configuration")

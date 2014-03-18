from django.db import models
from django.utils.translation import ugettext_lazy as _


class ReviewModel(models.Model):
    for_review = models.BooleanField(_('For review'), default=False)

    class Meta:
        abstract = True

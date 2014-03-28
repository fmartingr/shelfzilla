from django.db import models
from django.utils.translation import ugettext_lazy as _


class ReviewModel(models.Model):
    for_review = models.BooleanField(_('For review'), default=False)
    for_review_comment = models.TextField(
        _('Review comment'), null=True, blank=True)

    def first_letter(self):
        if hasattr(self, 'name'):
            return self.name and self.name[0] or ''

    class Meta:
        abstract = True

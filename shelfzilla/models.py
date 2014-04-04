from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class Model(models.Model):
    for_review = models.BooleanField(_('For review'), default=False)
    for_review_comment = models.TextField(
        _('Review comment'), null=True, blank=True)

    hidden = models.BooleanField(_('Hidden'), default=False)

    def first_letter(self):
        if hasattr(self, 'name'):
            return self.name and self.name[0] or ''

    def save(self, *args, **kwargs):
        # If model have a name and slug attribute, save slug
        # TODO set a model field to custom field name for slug creation
        if not getattr(self, 'slug', None) and getattr(self, 'name', None):
            self.slug = slugify(self.name)
        return super(Model, self).save(*args, **kwargs)

    class Meta:
        abstract = True

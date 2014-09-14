from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils.timezone import utc
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from django.utils.translation import activate


#
#   ENTRY
#
class Entry(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateTimeField(default=datetime.now(tz=utc))
    content = RichTextField()
    slug = models.SlugField(max_length=128)
    draft = models.BooleanField(default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name='author'
    )
    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def status(self):
        status = 'Published'

        if self.date > datetime.now(tz=utc):
            status = 'Scheduled'

        if self.draft:
            status = 'Draft'

        return status

    def get_absolute_url(self):
        kwargs = {
            'year': self.date.year,
            'month': self.date.strftime("%m"),
            'day': self.date.strftime("%d"),
            'slug': self.slug
        }
        url = reverse('blog:item', kwargs=kwargs)

        return url

    class Meta:
        app_label = 'blog'
        ordering = ['-date']
        verbose_name_plural = 'Entries'


#
#   TAG
#
class Tag(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=6, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'blog'
        ordering = ['name']



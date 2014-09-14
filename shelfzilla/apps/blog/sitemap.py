from datetime import datetime

from django.contrib.sitemaps import Sitemap

from .models import Entry


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(draft=False, date__lte=datetime.now())

    def lastmod(self, obj):
        return obj.date

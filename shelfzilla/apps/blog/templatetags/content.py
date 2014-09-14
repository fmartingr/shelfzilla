from django_jinja import library

from fmartingrcom.apps.config.models import SiteConfiguration


@library.filter
def readmore(content):
    config = SiteConfiguration.objects.get()
    summary, rest = content.split(config.readmore_tag, 1)
    return summary

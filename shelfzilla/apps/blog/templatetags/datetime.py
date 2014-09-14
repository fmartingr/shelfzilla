from pytz import timezone

from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.conf import settings

from django_jinja import library


@library.filter
def dt(t, fmt=None):
    """
    Call ``datetime.strftime`` with the given format string.
    """
    tz = timezone(settings.TIME_ZONE)
    if fmt is None:
        fmt = _('%B %e, %Y')
    return smart_unicode(tz.normalize(t).strftime(fmt)) if t else u''

from shelfzilla.apps.config.models import SiteConfiguration
from .models import User


def user_is_staff(request):
    return {
        'USER_IS_STAFF': request.user.is_staff
    }


def user_configuration(request):
    # TODO improve this shit
    use_pjax = True
    config = SiteConfiguration.objects.get()
    if not config.use_pjax:
        use_pjax = False

    return {
        'USER_CONFIG': {
            'show_admin_links': False,
            'use_pjax': use_pjax
        },
    }


def auth(request):
    result = {}
    if request.user.is_authenticated():
        result['user'] = User.objects.get(pk=request.user.pk)

    return result

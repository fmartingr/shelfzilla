from .models import User


def user_is_staff(request):
    return {
        'USER_IS_STAFF': request.user.is_staff
    }


def user_configuration(request):
    return {
        'USER_CONFIG': {
            'show_admin_links': False
        }
    }

def auth(request):
    result = {}
    if request.user.is_authenticated():
        result['user'] = User.objects.get(pk=request.user.pk)

    return result

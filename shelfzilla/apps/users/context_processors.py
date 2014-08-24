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

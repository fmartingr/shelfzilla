from .models import UserHaveVolume, UserWishlistVolume


def user_have_volumes(request):
    result = []
    if request.user.is_authenticated():
        result = UserHaveVolume.objects.filter(
            user=request.user).values_list('volume', flat=True)

    return {'user_have_volumes': result}


def user_wishlisted_volumes(request):
    result = []
    if request.user.is_authenticated():
        result = UserWishlistVolume.objects.filter(
            user=request.user).values_list('volume', flat=True)

    return {'user_wishlisted_volumes': result}

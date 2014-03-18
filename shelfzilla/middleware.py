from django.http import HttpResponseRedirect
from django.conf import settings


class BetaMiddleware(object):
    """
    Allow access only to people on the Beta group.
    """
    def process_request(self, request):
        beta_group_id = settings.BETA_ACCESS_GROUP_ID
        if request.user and not request.user.groups.filter(pk=beta_group_id):
            if request.path not in settings.BETA_ACCESS_ALLOW_URLS:
                return HttpResponseRedirect('/landing/')

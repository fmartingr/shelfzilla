from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from shelfzilla.apps.users.models import User
from shelfzilla.apps.manga.models import Volume


class HomepageView(View):
    template = 'homepage/home.html'

    def get(self, request):
        data = {}
        from datetime import datetime
        # TOP 5
        data['TOP_5_COLLECTORS'] = User.objects.filter(pk__gt=1)\
            .annotate(num_volumes=Count('have_volumes'))\
            .order_by('-num_volumes')[:5]

        # Latest manga
        data['LATEST_MANGA_ADDED'] = Volume.objects\
            .filter(release_date__lte=datetime.now())\
            .order_by('-release_date')[:6]

        # Future releases
        data['FUTURE_RELEASES'] = Volume.objects\
            .filter(release_date__gt=datetime.now())\
            .order_by('release_date')[:6]


        ctx = RequestContext(request, data)
        return render_to_response(self.template, context_instance=ctx)

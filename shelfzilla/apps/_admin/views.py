from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from shelfzilla.views import View
from shelfzilla.apps.manga.models import Volume, Series


class VolumeChangeSeriesView(View):
    template = '_admin/volumes/change_series.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        else:
            return super(VolumeChangeSeriesView, self).dispatch(
                request, *args, **kwargs)

    def get(self, request):
        volumes = Volume.objects.filter(
            pk__in=request.GET['volumes'].split(','))

        data = {
            'volumes': volumes,
            'series': Series.objects.all,
        }

        ctx = RequestContext(request, data)
        return render_to_response(self.template, context_instance=ctx)

    def post(self, request):
        volumes = Volume.objects.filter(
            pk__in=request.GET['volumes'].split(','))

        series = Series.objects.get(pk=int(request.POST['series_pk']))

        for vol in volumes:
            vol.series = series
            vol.save()

        messages.success(request, _('Volume series changed'))

        return HttpResponseRedirect('/admin/manga/volume/')

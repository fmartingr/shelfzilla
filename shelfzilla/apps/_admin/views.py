from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from filer.models import Image
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


class VolumeChangeCoverView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        else:
            return super(VolumeChangeCoverView, self).dispatch(
                request, *args, **kwargs)

    def post(self, request, volume_pk):
        try:
            volume = Volume.objects.get(pk=volume_pk)
            if 'cover_url' in request.POST:
                cover_url = request.POST['cover_url']

                from django.core.files.temp import NamedTemporaryFile
                from django.core.files import File
                import urllib2


                cover_temp = NamedTemporaryFile(delete=True)
                cover_temp.write(urllib2.urlopen(cover_url).read())
                cover_temp.flush()

                new_cover, is_new = Image.objects.get_or_create(file=File(cover_temp))
                # new_cover._move_file()

                if volume.cover:
                    volume.cover.delete()
                volume.cover = new_cover
                volume.save()

                messages.success(request, _('Volume series changed'))
            else:
                messages.error(request, _('Cover url to update not found.'))
        except Volume.DoesNotExist:
            messages.error(request, _('Volume not found.'))

        return HttpResponseRedirect(
            '/admin/manga/volume/{}/'.format(volume_pk))


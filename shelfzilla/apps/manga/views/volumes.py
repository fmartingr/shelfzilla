from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from ..models import Volume, UserWishlistVolume, UserHaveVolume
from .series import SeriesView


class WishlistVolumeView(SeriesView):
    template = 'manga/series/volumes/volume-pjax.html'

    def get(self, request, vid):
        volume = get_object_or_404(Volume, pk=vid)

        # Check if user already have this volume!
        try:
            UserHaveVolume.objects.get(volume=volume, user=request.user)
            messages.error(
                request,
                _('{} is already on your collection!').format(volume)
            )
        except UserHaveVolume.DoesNotExist:
            # Try to add to the wishlist...
            try:
                user_wish = UserWishlistVolume.objects.get(
                    volume=volume, user=request.user)
                user_wish.delete()
                messages.info(request,
                              _('{} removed from wishlist').format(volume))
            except UserWishlistVolume.DoesNotExist:
                # Or remove it if already in it!
                user_wish = UserWishlistVolume(
                    volume=volume, user=request.user)
                user_wish.save()
                messages.success(request, _('{} wishlisted!').format(volume))

        context = RequestContext(request, {'volume': volume})

        if context.get('is_pjax'):
            return render_to_response(self.template, context_instance=context)
        else:
            return HttpResponseRedirect(
                reverse('series.detail', args=[volume.series.pk])
            )


class HaveVolumeView(SeriesView):
    template = 'manga/series/volumes/volume-pjax.html'

    def get(self, request, vid):
        volume = get_object_or_404(Volume, pk=vid)

        try:
            user_have = UserHaveVolume.objects.get(
                volume=volume, user=request.user)
            user_have.delete()
            messages.info(request,
                          _('{} removed from collection.').format(volume))
        except UserHaveVolume.DoesNotExist:
            user_have = UserHaveVolume(volume=volume, user=request.user)
            user_have.save()
            messages.success(request,
                             _('{} added to collection!').format(volume))

            # Remove from wishlist if it exists
            try:
                user_wish = UserWishlistVolume.objects.get(
                    volume=volume, user=request.user)
                user_wish.delete()
            except UserWishlistVolume.DoesNotExist:
                pass

        context = RequestContext(request, {'volume': volume})

        if context.get('is_pjax'):
            return render_to_response(self.template, context_instance=context)
        else:
            return HttpResponseRedirect(
                reverse('series.detail', args=[volume.series.pk])
            )

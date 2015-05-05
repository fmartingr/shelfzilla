# coding: utf-8

# django
from django import forms
from django.utils.translation import ugettext as _

# app
from . import models


class SuggestVolumeForm(forms.ModelForm):
    """
    Form used by users to add a volume that we don't have.
    """
    class Meta:
        model = models.Volume
        fields = (
            'number', 'name',
            'publisher',
            'language',
            'pages',
            'retail_price',
            'isbn_10', 'isbn_13', )
        help_texts = {
            'number': _("The number of this volume."),
            'name': _("Volumes without a number usually have a name instead."),
        }

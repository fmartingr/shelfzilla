# coding: utf-8
import json
import os
import sys
import requesocks as requests
import uuid
import re
from utils.crawler_listadomanga.progressbar import ProgressBar
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shelfzilla.settings.local")
from filer.models.imagemodels import Image
from django.core.files import File
import datetime


from shelfzilla.apps.manga.models import Series, Person, Publisher, Volume, Language, SeriesSummary, SeriesPublisher, VolumeCollection


esp = Language.objects.get(code='es-es')
cat = Language.objects.get(code='es-ca')

#
# MIGRATE SUMMARIES
#
# series = Series.objects.all()
# for s in series:
#     language = esp
#     if u'Catalán' in s.name:
#         language = cat

#     summary, is_new = SeriesSummary.objects.get_or_create(
#         series=s, language=language, summary=s.summary
#     )
# empty = SeriesSummary.objects.filter(summary=None).delete()
# empty = SeriesSummary.objects.filter(summary="").count()

#
# ADD NEW PUBLISHERS INFO
#
# series = Series.objects.all()
# for s in series:
#     i = 1
#     for pub in s.publishers_old.all():
#         if i == 1:
#             current = True
#         else:
#             current = False
#         pub_new, is_new = SeriesPublisher.objects.get_or_create(
#             series=s, publisher=pub, status=s.status, actual_publisher=current
#         )
#         i += 1


#
# MIGRATE CATALA SERIES TO SERIES NAME
#
# series_catala = Series.objects.filter(name__contains=u'Catalán')
# print(series_catala)

# # series_catala = Series.objects.filter(pk=1284)
# for s in series_catala:
#     name_corrected = " ".join(s.name.split(' ')[:-1])
#     print(s.name.encode('utf-8'))
#     print(name_corrected.encode('utf-8'))
#     try:
#         correct_series = Series.objects.get(name=name_corrected)

#         for vol in s.volumes.all():
#             vol.series = correct_series
#             vol.save()

#         for summary in s.summaries.all():
#             summary.series = correct_series
#             summary.save()

#         for pub in s.publishers.all():
#             if correct_series.publishers.filter(publisher=pub.publisher).count() > 0:
#                 update_spub = correct_series.publishers.filter(publisher=pub.publisher)[0]
#             else:
#                 update_spub = SeriesPublisher.objects.create(
#                     series=correct_series, publisher=pub.publisher, status=s.status
#                 )

#             update_spub.status = s.status
#             update_spub.save()

#         s.delete()
#     except Series.DoesNotExist:
#         # Rename series if only in csatalá
#         s.name = name_corrected
#         s.save()


#
#   UPDATE VOLUMES WITHOUT LANGUAGE TO ESP
#
# volumes_not = Volume.objects.filter(language=None).update(language=esp)

#
#   INSERT VOLUMES INTO COLLECTIONS
#
# pattern = re.compile('\((.*)\)')
# series = Series.objects.all()
# for s in series:
#     delete_this_series = False
#     if u'Catalán' not in s.name:
#         if '(' in s.name:
#             print(s.name.encode('utf-8'))
#             m = pattern.search(s.name)
#             special_name = m.group()
#             col_name = special_name.replace('(', '').replace(')', '')
#             name = s.name.split(' (')[0]


#             # Look for series name without (asdjaslkdjasd)
#             try:
#                 series = Series.objects.get(name=name)
#                 collection = VolumeCollection.objects.create(
#                     name=col_name, series=series
#                 )

#                 for pub in s.publishers.all():
#                     if series.publishers.filter(publisher=pub.publisher).count() > 0:
#                         update_spub = series.publishers.filter(publisher=pub.publisher)[0]
#                     else:
#                         update_spub = SeriesPublisher.objects.create(
#                             series=series, publisher=pub.publisher, status=s.status
#                         )
#                     update_spub.status = s.status
#                     update_spub.save()

#                 for vol in s.volumes.all():
#                     vol.series = series
#                     vol.collection = collection
#                     vol.save()

#                 delete_this_series = True
#             except Series.DoesNotExist:
#                 series = s
#                 series.name = name
#                 series.slug = None
#                 series.save()

#                 collection = VolumeCollection.objects.create(
#                     name=col_name, series=series, default=True
#                 )

#                 for vol in s.volumes.all():
#                     vol.collection = collection
#                     vol.save()


#             if delete_this_series:
#                 s.delete()

#
#   MAKE ALL CREATED COLLECTIONS NOT DEFAULT EXCEPT THE ONES NAMED TOMOS
#
# VolumeCollection.objects.all().update(default=False)
# VolumeCollection.objects.filter(name='Tomos').update(default=True)

#
#   ALL VOLUMES WITHOUT A COLLECTION SHOULD BE NAMED 1º Edicion
#

# volumes = Volume.objects.filter(collection=None)
# for vol in volumes:
#     col, is_new = VolumeCollection.objects.get_or_create(
#         series=vol.series, default=True, name='1ª Edición'
#     )
#     vol.collection = col
#     vol.save()


#
#   REMOVE COLLECTIONS WITHOUT VOLUMES
#
# from django.db.models import Count
# collections = VolumeCollection.objects
# collections_wo_vols = VolumeCollection.objects.all()\
#     .annotate(num_volumes=Count('volumes'))\
#     .filter(num_volumes__eq=0)

# collections_wo_vols.delete()

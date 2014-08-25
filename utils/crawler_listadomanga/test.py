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
import warnings
import datetime
warnings.filterwarnings('ignore')
buff = ''
with open('utils/crawler_listadomanga/data.json', 'r') as f:
    buff += f.read()

new_json = json.loads(buff)

pb_total = {
    'end': len(new_json),
    'width': 50,
    'fill': '#',
    'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

r_unwanted = re.compile("[\n\t\r]")
total_pb = ProgressBar(**pb_total)

session = requests.session()
session.proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

DATE_VALUES = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
}

def download_file(url):
    local_filename = "/tmp/{}".format(str(uuid.uuid4()))
    # local_filename = str(uuid.uuid4())
    # NOTE the stream=True parameter
    download_errors = True
    redownload_cover = False
    while download_errors:
        # Change TOR identity
        if redownload_cover:
            print('=> RENEWING TOR IDENTITY...')
            from stem import Signal
            from stem.control import Controller

            with Controller.from_port(port=9051) as controller:
                controller.authenticate("1234")
                controller.signal(Signal.NEWNYM)

            redownload_cover = False

        try:
            r = session.get(url)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

            if os.path.getsize(local_filename) < 200:
                check_cover = open(local_filename, 'r')
                if 'blacklisted' in check_cover.read():
                    redownload_cover = True
                    old_cover = vol.cover
                    vol.cover = None
                    vol.save()
                    old_cover.delete()
                else:
                    download_errors = False
            else:
                download_errors = False
        except:
            redownload_cover = True
            download_errors = True

    return local_filename


def clear():
    os.system('clear')


def update_pbs(title):
    clear()
    print('{}'.format(total_pb))
    print('Now working: {}'.format(title.encode('utf-8')))


# filename = download_file('http://ifconfig.me/ip')
# os.remove(filename)


i = 0
from shelfzilla.apps.manga.models import Series, Person, Publisher, Volume, Language
for s in new_json:
    is_catala = False
    update_pbs(s['name'])

    if '(' in s['name']:
        # TODO collections!
        pass

    serie, is_new = Series.objects.get_or_create(
        name=s['name']
    )

    # Replaces
    if 'spanish_publisher' in s:
        if u'Editores de Tebeos' in s['spanish_publisher']:
            s['spanish_publisher'] = u'Ediciones Glénat / EDT'
        if u'ECC Ediciones' in s['spanish_publisher']:
            s['spanish_publisher'] = u'El Catálogo del Cómic'



    # TODO collections

    # print("================== {}".format(serie.name.encode('utf-8')))

    # Summary
    if s['summary'] != '':
        serie.summary = s['summary']

    # Completed series
    # TODO catala?
    if 'spanish_numbers' in s:
        if 'completa' in s['spanish_numbers']:
            serie.finished = True
            serie.status = 'finished'

        if 'cancelada' in s['spanish_numbers']:
            serie.status = 'cancelled'

    if 'catala_numbers' in s:
        is_catala = True
        if 'completa' in s['catala_numbers']:
            serie.finished = True
            serie.status = 'finished'

        if 'cancelada' in s['catala_numbers']:
            serie.status = 'cancelled'

    # Art
    if 'art' in s and s['art']:
        art = s['art'].split(',')
        for person in art:
            name = person.strip()
            art, is_new = Person.objects.get_or_create(
                name=name
            )
            serie.art.add(art)

    # Story
    if 'story' in s and s['story']:
        story = s['story'].split(',')
        for person in story:
            name = person.strip()
            story, is_new = Person.objects.get_or_create(
                name=name
            )
            serie.story.add(story)

    # Spanish publisher
    if 'spanish_publisher' in s and s['spanish_publisher']:
        pub, is_new = Publisher.objects.get_or_create(
            name=s['spanish_publisher']
        )
        if s['spanish_publisher_url']:
            pub.url = s['spanish_publisher_url']
            pub.save()

    # Japanese publisher
    if 'japanese_publisher' in s and s['japanese_publisher']:
        src_pub, is_new = Publisher.objects.get_or_create(
            name=s['japanese_publisher']
        )
        if s['japanese_publisher_url']:
            src_pub.url = s['japanese_publisher_url']
            src_pub.save()

        serie.original_publisher = src_pub

    # Volumes
    if len(s['published_volumes']) > 0:
        for index, volume in enumerate(s['published_volumes']):

            try:
                number = int(volume['name'].split(u'\u00ba')[1])
            except:
                number = index
            print('[volume] {}'.format(r_unwanted.sub(" ", volume['name'].encode('utf-8'))))

            try:
                vol, is_new = Volume.objects.get_or_create(
                    series=serie,
                    number=number,
                    publisher=pub
                )

                if is_catala:
                    language = Language.objects.get(code='es-ca')
                    vol.language = language
                    vol.save()

                if 'date' in volume:
                    month, year = volume['date'].split(' ')
                    month = DATE_VALUES[month]
                    year = int(year)

                    vol.release_date = datetime.datetime(year, month, 1)
                    vol.save()

                if vol.cover:
                    file_path = vol.cover.file.path
                    if os.path.getsize(file_path) < 200:
                        check_cover = open(file_path, 'r')
                        if 'blacklisted' in check_cover.read():
                            old_cover = vol.cover
                            vol.cover = None
                            vol.save()
                            old_cover.delete()

                if 'cover' in volume and not vol.cover:
                    cover_file = download_file(volume['cover'])
                    check_local_file = open(cover_file, 'r')
                    if not 'blacklisted' in check_local_file.read():
                        with open(cover_file) as f:
                            dj_file = File(f, name=str(uuid.uuid4()))

                            cover, is_new_cover = Image.objects.get_or_create(
                                folder=None,
                                name=str(uuid.uuid4()),
                                file=dj_file
                            )

                            vol.cover = cover
                            vol.save()
                    else:
                        print('BLACKLISTED!')
                        print(cover_file)
                        quit()

            except Exception as error:
                print('Error: {}'.format(error))
    serie.save()
    total_pb += 1
    sys.stdout.flush()

    i += 1

    # if i == 20:
    #     break

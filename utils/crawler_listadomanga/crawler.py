from StringIO import StringIO
from datCrawl.crawlers import Crawler
from lxml import etree
from datetime import date
from pprint import pprint


class ListadoManga(Crawler):
    urls = [
        ('get_manga', '(?P<url>^http\:\/\/www\.listadomanga\.es\/coleccion\.php(.*)$)'),
        ('get_links', '(?P<url>^http\:\/\/www\.listadomanga\.es\/lista\.php\?genero=\d+)'),
    ]
    downloader = 'DefaultDownloader'

    base = 'http://www.listadomanga.es'

    _info = {
        'site_name': 'ListadoManga',
        'crawler_key': 'listadomanga',
        'language': 'en'
    }

    _constant = {}

    def action_get_links(self, data, **kwargs):
        ids = []

        document = etree.parse(
            StringIO(data),
            etree.HTMLParser(encoding='utf-8')
        )
        root = document.getroot()

        for link in root.xpath("//a/@href"):
            if "coleccion" in link:
                ids.append(int(link.split('=',2)[1]))

        return ids

    def action_get_manga(self, data, **kwargs):
        obj = {}

        document = etree.parse(
            StringIO(data),
            etree.HTMLParser(encoding='utf-8')
        )

        root = document.getroot()

        try:
            # Details TD
            keys = [
                ('original', 'original_title'),
                ('Gui', 'story'),
                ('Dibujo', 'art'),
                ('Editorial japonesa', 'japanese_publisher'),
                ('Editorial espa', 'spanish_publisher'),
                ('Colecci', 'collection'),
                ('Formato', 'format'),
                ('Sentido de lectura', 'read_direction'),
                ('meros en japo', 'japanese_numbers'),
                ('meros en espa', 'spanish_numbers'),
                ('meros en cata', 'catala_numbers'),
                ('Nota', 'note'),
            ]
            td = root.xpath('//table//td[@class="izq"][contains(.,"original")]')
            first = True
            td_contains = {}
            last = None
            for t in td[0].itertext():
                text = t.strip()
                if t.strip():
                    if first:
                        first = False
                        obj['name'] = text
                    else:
                        if ':' in text:
                            last = text.split(':')[0]
                            td_contains[last] = u''
                        else:
                            td_contains[last] += text

            for tdkey, row in td_contains.iteritems():
                for key in keys:
                    if key[0] in tdkey:
                        obj[key[1]] = row.split('(web oficial)')[0]

            # Japanese publisher URL
            try:
                jap = root.xpath("//td[contains(., 'Editorial jap')]//text()[contains(., 'Editorial jap')]/following::a")[1]
                obj['japanese_publisher_url'] = jap.attrib['href']
            except:
                obj['japanese_publisher_url'] = ''

            # Spanish publisher URL
            try:
                esp = root.xpath("//td[contains(., 'Editorial esp')]//text()[contains(., 'Editorial esp')]/following::a")[1]
                obj['spanish_publisher_url'] = esp.attrib['href']
            except:
                obj['spanish_publisher_url'] = ''

            # Un/Published volumes
            obj['published_volumes'] = []
            obj['unpublished_volumes'] = []
            vols = root.xpath("//table[contains(., 'editados')]/following-sibling::table//td[not(contains(@class, 'separacion'))]//table//td[@class='cen']")
            for vol in vols:
                published = False
                volume = {}
                image = vol.find('img')
                volume['cover'] = "{}/{}".format(self.base, image.attrib['src'])

                text = []

                if vol.find('hr') is not None:
                    for dom in vol.iterchildren():
                        if dom.tag == 'hr':
                            break
                        else:
                            if dom.text:
                                text.append(dom.text)
                            elif dom.tail:
                                text.append(dom.tail)
                else:
                    text = list(vol.itertext())

                if len(text) >= 4:
                    volume['date'] = text.pop(-1).strip()

                    price = text.pop(-1)
                    if 'ratuito' in price:
                        volume['price'] = 0
                    else:
                        volume['price'] = float(price.split(' ')[0].replace(',', '.'))
                    volume['pages'] = text.pop(-1).strip()
                    published = True

                volume['name'] = ("".join(text)).strip()

                if published:
                    obj['published_volumes'].append(volume)
                else:
                    obj['unpublished_volumes'].append(volume)

            # Description
            try:
                obj['summary'] = root.xpath("//h2[contains(., 'Sinopsis')]/../text()")[0].strip()
            except:
                obj['summary'] = ''
        except Exception as error:
            print("Error with: {}".format(obj['name'].encode('utf-8')))
            print("---------- {}".format(error))
            obj = 'Error'

        # pprint(obj)

        return obj

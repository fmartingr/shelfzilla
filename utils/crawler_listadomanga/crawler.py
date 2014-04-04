from StringIO import StringIO
from datCrawl.crawlers import Crawler
from lxml import etree
from datetime import date
from pprint import pprint


class ListadoManga(Crawler):
    urls = [
        ('get_manga', '(?P<url>^http\:\/\/www\.listadomanga\.es\/coleccion\.php(.*)$)'),
        ('get_links', '(?P<url>^http\:\/\/www\.listadomanga\.es\/lista\.php)'),
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

        ''' Get Info '''
        try:
            obj['title'] = root.xpath('//td[@class="izq"]/h2/text()')[0].strip()
            obj['dash'] = root.xpath('//td[@class="izq"]/a/text()')[0]
            obj['cartoonist'] = root.xpath('//td[@class="izq"]/a/text()')[1]
            obj['src_editorial'] = root.xpath('//td[@class="izq"]/a/text()')[2]
            obj['src_ed_website'] = root.xpath('//td[@class="izq"]/a/@href')[3]
            obj['editorial'] = root.xpath('//td[@class="izq"]/a/text()')[4]
            obj['ed_website'] = root.xpath('//td[@class="izq"]/a/@href')[5]
            obj['ed_collection'] = root.xpath('//td[@class="izq"]/a/text()')[6]
            obj['sinopsis'] = root.xpath("//h2[contains(., 'Sinopsis')]/../text()")
            
        

            ''' Get Image link and info'''
            # Edited numbers
            obj['zz_data_sets_published'] = []
            obj['zz_data_sets_unpublished'] = []
            package = {}
            data = root.xpath('/html/body/center/center[1]/table[3]/tr/td//text()')
            links = root.xpath('/html/body/center/center[1]/table[3]//@src')

            for element in links:
                package['edited_image_link'] = self.base + "/" +element
                package['title'] = data.pop(0)
                package['pages'] = data.pop(0)
                package['price'] = data.pop(0)
                package['date'] = data.pop(0)
                obj['zz_data_sets_published'].append(package.copy())
                
            package = {}
            check = root.xpath('/html/body/center/center[1]/table[4]//text()')
            if u'N\xfameros en preparaci\xf3n:' in check:
                links = root.xpath('/html/body/center/center[1]/table[5]//@src')
                titles = root.xpath('/html/body/center/center[1]/table[5]//text()')
                for element in links:
                    package['no_edited_image_link'] = self.base + element
                    package['title'] = titles.pop(0)
                    obj['zz_data_sets_unpublished'].append(package.copy())

            return obj

        except:
            return "Error"

        
                    



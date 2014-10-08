# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from shelfzilla.items import VolumeItem



class PaninicomicsSpider(CrawlSpider):
    name = "paninicomics"
    allowed_domains = ["www.paninicomics.es", "paninicomics.es"]
    start_urls = (
        'http://www.paninicomics.es/web/guest/manga/colecciones/',
    )

    rules = (
        # Catalog details
        # Bleach collection: http://www.paninicomics.es/web/guest/coleccion_titulos?category_id=181341
        Rule(
            LinkExtractor(
                allow=(
                    '\/web\/guest\/coleccion\_titulos\?category\_id\=\d+'
                ),
                allow_domains=allowed_domains,
                canonicalize=False
            ),
        ),

        Rule(
            LinkExtractor(
                allow=(
                    '\/web\/guest\/titulo\_detail\?viewItem\=\d+'
                ),
                canonicalize=False
            ),
            callback='parse_tome'
        ),
    )

    _base_url = 'http://www.paninicomics.es'
    _publisher_name = 'Panini Comics'

    def parse_start_url(self, response):
        #print response.url
        pass


    def parse_tome(self, response):
        item = VolumeItem()

        item['url'] = response.url
        item['publisher_name'] = self._publisher_name

        ## Serie Name and volume name
        name_raw = response.xpath('//*[@class="title"]/h3/text()').extract()
        name = str(name_raw)[3:-2]
        cleaned_name = str(name).split(' ')[0:-1]
        item['series_name'] = ' '.join(cleaned_name)
        list_raw_name = response.xpath('//*[@class="title"]/h4//text()').extract()
        item['name'] = str(list_raw_name[1]).strip("\n \' [ ]")

        ## Tome number
        item['number'] = str(name).split(' ')[-1]

        ## Cover
        image_link = str(response.xpath('//*[@class="cover"]/img/@src').extract()).strip("\' [ ] ")[2:-1]
        item['cover'] = self._base_url + image_link
        
        ## ISBN and Pages
        numbers = response.xpath('//*[@class="features"]/text()').extract()
        pages = re.findall(r'\d{3}', str(numbers))
        if len(pages) > 3:
            item['pages'] = pages[-1]

        else:
            item['pages'] = pages[0]            
        item['isbn_13'] = str(re.findall(r'\d{13}', str(numbers))).strip("\' [] ")

        print item













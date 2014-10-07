# -*- coding: utf-8 -*-
import scrapy
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

    _publisher_name = 'Panini Comics'

    def parse_start_url(self, response):
        #print response.url
        pass


    def parse_tome(self, response):
        item = VolumeItem()

        item['url'] = response.url
        item['publisher_name'] = self._publisher_name
        item['isbn_13'] = response.xpath('//*[@class="features"]/text()').extract()
        #item['pages'] = response.xpath('//*[@id="shop"]/div[2]/div[3]/p[2]/text()').extract()

        print item
        #response.xpath('//*[@id="shop"]/div[2]/div[3]/h3/text()').extract()
















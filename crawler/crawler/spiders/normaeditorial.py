# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.items import VolumeItem


def join_strings(string_list, convert_to=None):
    def convert(value):
        if convert_to:
            return convert_to(value)
        return value
    return convert("".join(string_list))


class NormaeditorialSpider(CrawlSpider):
    name = "normaeditorial"
    allowed_domains = ["normaeditorial.com", "www.normaeditorial.com"]
    start_urls = (
        'http://www.normaeditorial.com/catalogo.asp?T/5/0/0/Catalogo_Manga',
    )
    rules = (
        # Catalog details
        # Series: /catalogo.asp?S/3203/0/0/fullmetal_alchemist_kanzenban
        # Page: /catalogo.asp?T/5/0/0,D/
        Rule(LinkExtractor(
                allow=(
                    '\/catalogo\.asp\?(\w)\/5\/\d\/\d\/[\w\d\_]+',
                    '\/catalogo\.asp\?(\w)\/5\/\d\/[\d\,\w]+\/',
                    '\/catalogo\.asp\?(\w)\/5\/\d\/[\d\,\w]+',
                ),
                allow_domains=allowed_domains,
                canonicalize=False
            )
        ),
        # Next releases
        Rule(LinkExtractor(
                allow=("\/blogmanga\/blog\/\?page_id\=275",),
                canonicalize=False
            ),
            callback="parse_next_releases"
        ),
        # Volume details
        # /ficha.asp?0/0/012770008/0/fullmetal_alchemist_kanzenban_08
        Rule(LinkExtractor(
                allow=(
                    '\/ficha\.asp\?(\d+)\/(\d+)\/(\d+)\/(\d+)\/([\w\d\_\.\-]+)',
                ),
                allow_domains=allowed_domains,
                canonicalize=False
            ),
            callback='parse_volume'
        ),
    )

    _publisher_name = 'Norma Editorial'

    def parse_start_page(self, response):
        pass

    def parse_volume(self, response):
        item = VolumeItem()

        item['url'] = response.url
        item['publisher_name'] = self._publisher_name
        item['series_name'] = response.xpath(
            '//div[@id="basic_info"]/h2[contains(., "Serie")]/a/text()'
        ).extract()[0].strip()

        pairs = (
            ('size', 'Tama'),
            ('color', 'Color'),
            ('isbn', 'ISBN'),
            ('price', 'PVP'),
        )

        not_released = response.xpath('//div[@id="basic_info"]/h2/img[@alt="proximamente"]')

        if len(not_released) > 0:
            item['not_released'] = True

        for k, v in pairs:
            try:
                item[k] = response.xpath(
                    '//div[@id="basic_info"]/h3[contains(., "{}")]/span/text()'.format(v)
                ).extract()[0].strip()
            except IndexError:
                pass

        big_name = response.xpath('//div[@id="basic_info"]/h1/text()')\
            .extract()[0].strip()

        try:
            item['number'] = int(big_name.replace(item['series_name'], '').strip())
        except:
            item['name'] = big_name.replace(item['series_name'], '').strip()

        item['cover'] = response.xpath('//div[@id="SUB_centro_IZ_FICHA_MENU_im"]/img/@src').extract()[0]

        # Other
        if 'name' in item and 'pack' in item['name'].lower():
            item['hide'] = True
            item['is_pack'] = True

        # TEST
        item['uuid'] = big_name

        yield item

    def parse_next_releases(self, request):
        pass

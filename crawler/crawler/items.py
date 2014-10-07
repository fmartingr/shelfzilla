# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See docum1entation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VolumeItem(scrapy.Item):
    uuid = scrapy.Field()
    url = scrapy.Field()
    publisher_name = scrapy.Field()
    series_name = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    format = scrapy.Field()
    size = scrapy.Field()
    pages = scrapy.Field()
    color = scrapy.Field()

    isbn = scrapy.Field()
    isbn_10 = scrapy.Field()
    isbn_13 = scrapy.Field()

    price = scrapy.Field()

    hide = scrapy.Field()
    is_pack = scrapy.Field()
    not_released = scrapy.Field()

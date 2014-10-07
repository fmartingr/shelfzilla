# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        if item['uuid'] in self.seen:
            raise DropItem("Duplicate found: %s" % item)
        else:
            self.seen.add(item['uuid'])
            return item


class CheckLanguagePipeline(object):
    def process_item(self, item, spider):
        if u'CATALÁN' in item['uuid'].upper():
            raise DropItem("Not supported language: %s" % item)
        else:
            return item


class CleanFieldsPipeline(object):
    fields = ('isbn', 'price', )

    def clean_isbn(self, item):
        isbn = item['isbn'].replace('-', '')

        if len(isbn) < 13:
            isbn = isbn[0:10]

        return isbn

    def clean_price(self, item):
        price = float(item['price'][:-1].replace(',', '.'))

        return price


    def process_item(self, item, spider):
        for field in self.fields:
            if field in item:
                item[field] = getattr(self, 'clean_%s' % field)(item)

        return item

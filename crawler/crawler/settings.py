# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {
    # Check duplicate
    # Determine if other language than Spanish (drop them if is)
    # Clean fields
    'crawler.pipelines.DuplicatesPipeline': 100,
    'crawler.pipelines.CheckLanguagePipeline': 200,
    'crawler.pipelines.CleanFieldsPipeline': 300,
    # ...
    'scrapycouchdb.CouchDBPipeline': 1000,
}



COUCHDB_SERVER = 'http://127.0.0.1:5984/'
COUCHDB_DB = 'norma'
COUCHDB_UNIQ_KEY = 'uuid'
COUCHDB_IGNORE_FIELDS = []

LOG_LEVEL = 'ERROR'
LOG_FILE = 'scrapy.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Test Crawler (+http://www.yourdomain.com)'

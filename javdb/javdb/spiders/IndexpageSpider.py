import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
import time


class IndexPageSpider(scrapy.Spider):
    name = 'index_page'
    start_urls = ['https://javdb40.com']
    custom_settings = {
        "LOG_FILE": "./logs/index_page.log",
        "ITEM_PIPELINES": {
            'javbus.pipelines.IndexPagePipeline': 300,
        }
    }

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass

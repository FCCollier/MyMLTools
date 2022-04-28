import scrapy
import logging
from ..items import IndexpageItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
import time


class IndexPageSpider(scrapy.Spider):
    name = 'index_page'
    start_urls = [
        'https://javdb40.com/censored',
    ]
    custom_settings = {
        "LOG_FILE": "./logs/indexpage.log",
        "ITEM_PIPELINES": {
            'javdb.pipelines.IndexpagePipeline': 300,
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.warning("A" * 60)
        logging.warning("IndexPage爬虫开始！")

    def __del__(self):
        logging.warning("IndexPage爬虫结束！")
        logging.warning("A" * 60)

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        logging.warning("B" * 60)
        logging.warning("索引页开始爬取！：" + str(response.url))

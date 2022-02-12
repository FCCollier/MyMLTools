import scrapy
from scrapy.loader import ItemLoader
from ..items import LatestUrlItem
import logging
from ..settings import *
import pandas as pd
from sqlalchemy import create_engine
from .JavBusSpider import JavBusConfig
import time


class LastUrlSpider(scrapy.Spider):
    name = 'last_url'
    start_urls = ['https://www.busfan.club']
    custom_settings = {
        "LOG_FILE": "./logs/last_url.log",
        "ITEM_PIPELINES": {
            'javbus.pipelines.LastUrlPipeline': 300,
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.warning("A" * 60)
        logging.warning("LastUrl爬虫开始！")

    def __del__(self):
        logging.warning("LastUrl爬虫结束！")
        logging.warning("A" * 60)

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse, errback=JavBusConfig.parse_err)

    def parse(self, response, **kwargs):
        logging.warning("B" * 60)
        logging.warning("最新地址页开始爬取！：" + str(response.url))
        # /html/body/div[5]
        url_selectors = response.xpath("/html/body/div[4]/div/div[2]/div/div")
        for url_selector in url_selectors:
            # /html/body/div[4]/div/div[2]/div/div[1]/a
            latest_url_item = ItemLoader(item=LatestUrlItem(), selector=url_selector)
            latest_url_item.add_xpath("url", "a/text()")
            latest_url_item.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            yield latest_url_item.load_item()
        logging.warning("最新地址页爬取完毕！：" + str(response.url))
        logging.warning("B" * 60)
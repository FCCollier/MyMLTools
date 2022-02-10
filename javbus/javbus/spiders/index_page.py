import scrapy
import logging
from ..items import IndexPageItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from .JavBusSpider import JavBusConfig
import time


class IndexPageSpider(scrapy.Spider):
    name = 'index_page'
    start_urls = ['https://www.busfan.club']
    custom_settings = {
        "LOG_FILE": "./logs/index_page.log",
        "ITEM_PIPELINES": {
            'javbus.pipelines.IndexPagePipeline': 300,
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
            yield scrapy.Request(url=start_url, callback=self.parse, errback=JavBusConfig.parse_err)

    def parse(self, response, **kwargs):
        logging.warning("B" * 60)
        logging.warning("索引页开始爬取！：" + str(response.url))
        # //*[@id="waterfall"]/div
        list_selector = response.xpath("//a[@class='movie-box']")
        for one_selector in list_selector:
            pageitem = ItemLoader(item=IndexPageItem(), selector=one_selector)
            # //*[@id="waterfall"]/div[1]/a/div[2]/span/date[1]
            pageitem.add_xpath("video_id", "div[@class='photo-info']/span/date[1]/text()")
            # //*[@id="waterfall"]/div[1]/a/div[1]/img
            pageitem.add_xpath("video_title", "div[@class='photo-frame']/img/@title")
            # //*[@id="waterfall"]/div[1]/a
            pageitem.add_xpath("video_url", "@href")
            pageitem.add_xpath("premiered", "div[@class='photo-info']/span/date[2]/text()")
            pageitem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            yield pageitem.load_item()
        logging.warning("索引页爬取完毕！：" + str(response.url))
        logging.warning("B" * 60)

        le = LinkExtractor(restrict_xpaths="//*[@id='next']")
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(url=next_url, callback=self.parse, errback=JavBusConfig.parse_err)
        else:
            logging.warning("索引页不存在或者到底！:" + str(response.url))
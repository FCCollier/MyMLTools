from scrapy import Request
from scrapy.spiders import Spider
from ..items import VideoPageItem
from scrapy.loader import ItemLoader
import time
from ..settings import *
import logging
import requests


class JavBusSpider(Spider):
    name = "javbus"

    def start_requests(self):
        start_urls = START_URLS
        for start_url in start_urls:
            try:
                requests.get(start_url)
            except requests.exceptions.ConnectionError as e:
                logging.error("起始页面无法获取！错误信息：" + str(e))
                logging.error("起始页面无法获取！页面地址：" + start_url)
            else:
                yield Request(url=start_url, callback=self.video_page_parse, meta={"url": start_url})
                logging.info(msg="起始页面压入：" + start_url)

    def get_detail_requests(self):
        pass

    def get_actress_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass

    def video_page_parse(self, response, **kwargs):
        # //*[@id="waterfall"]/div
        list_selector = response.xpath("//a[@class='movie-box']")
        for one_selector in list_selector:
            pageitem = ItemLoader(item=VideoPageItem(), selector=one_selector)
            # //*[@id="waterfall"]/div[1]/a/div[2]/span/date[1]
            pageitem.add_xpath("video_id", "div[@class='photo-info']/span/date[1]/text()")
            # //*[@id="waterfall"]/div[1]/a/div[1]/img
            pageitem.add_xpath("video_title", "div[@class='photo-frame']/img/@title")
            # //*[@id="waterfall"]/div[1]/a
            pageitem.add_xpath("video_url", "@href")
            pageitem.add_xpath("pub_date", "div[@class='photo-info']/span/date[2]/text()")
            pageitem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            yield pageitem.load_item()

        # //*[@id="next"]
        if response.xpath("//*[@id='next']/@href").extract_first() is not None:
            next_url = response.meta["url"] + response.xpath("//*[@id='next']/@href").extract_first()
            logging.info(msg=str("索引页地址：" + next_url))
            yield Request(url=next_url, callback=self.video_page_parse, meta={"url": response.meta["url"]})
        else:
            logging.warning("索引页不存在或者到底！:" + str(response.url))

    def video_parse(self, response, **kwargs):
        # //tr[contains(@class,'result')]
        pass

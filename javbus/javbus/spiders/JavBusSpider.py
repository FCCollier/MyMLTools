from scrapy import Request
from scrapy.spiders import Spider
from ..items import VideoPageItem
from ..items import LatestUrlItem
from scrapy.loader import ItemLoader
import time
import logging
from ..settings import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class JavBusSpider(Spider):
    name = "javbus"

    def start_requests(self):
        start_urls = START_URLS
        for start_url in start_urls:
            yield Request(url=start_url, callback=self.video_page_parse, errback=self.parse_err,
                          meta={"url": start_url})

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
        logging.warning("页面信息已提交！" + str(response.url))

        # //*[@id="next"]
        if response.xpath("//*[@id='next']/@href").extract_first() is not None:
            next_url = response.meta["url"] + response.xpath("//*[@id='next']/@href").extract_first()
            logging.warning(msg=str("索引页地址：" + next_url))
            yield Request(url=next_url, callback=self.video_page_parse, errback=self.parse_err,
                          meta={"url": response.meta["url"]})
        else:
            logging.warning("索引页不存在或者到底！:" + str(response.url))
            # /html/body/div[4]/div/div[2]/div/div
            url_selectors = response.xpath("/html/body/div[4]/div/div[2]/div/div")
            for url_selector in url_selectors:
                # /html/body/div[4]/div/div[2]/div/div[1]/a
                latest_url_item = ItemLoader(item=LatestUrlItem(), selector=url_selector)
                latest_url_item.add_xpath("url", "a/text()")
                latest_url_item.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                yield latest_url_item.load_item()
            logging.warning("最新地址列表已提交！")

    def video_parse(self, response, **kwargs):
        # //tr[contains(@class,'result')]
        pass

    def parse_err(self, failure):
        print('*' * 30)
        # log all failures
        logging.error("JavBusSpider 错误！")
        logging.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            logging.error('错误类型： HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            logging.error('错误类型：DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logging.error('错误类型：TimeoutError on %s', request.url)

        else:
            logging.error('错误类型：其他错误。')

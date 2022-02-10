import scrapy
import logging
from ..items import IndexPageItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import time


class IndexPageSpider(scrapy.Spider):
    name = 'index_page'
    start_urls = ['https://www.busfan.club']
    custom_settings = {
        "LOG_FILE": "./index_page.log",
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
            yield scrapy.Request(url=start_url, callback=self.parse, errback=self.parse_err)

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
            yield scrapy.Request(url=next_url, callback=self.parse, errback=self.parse_err)
        else:
            logging.warning("索引页不存在或者到底！:" + str(response.url))

    def parse_err(self, failure):
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
import scrapy.loader
from scrapy import Request
from scrapy.spiders import Spider
from ..items import LatestUrlItem
from ..items import VideoItem
from ..items import IndexPageItem
from scrapy.loader import ItemLoader
import time
import logging
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import platform


class JavBusSpider(Spider):
    name = "javbus"
    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.warning("爬虫开始！")

    def __del__(self):
        logging.warning("爬虫结束！")

    def start_requests(self):

        logging.warning("起始页开始爬取！！")
        for start_url in self.start_urls:
            logging.warning("起始页准备压入！：" + str(start_url))
            yield Request(url=start_url, callback=self.video_page_parse, errback=self.parse_err,
                          meta={"url": start_url})
            logging.warning("起始页已压入！：" + str(start_url))
        logging.warning("起始页爬取完毕！")

    def parse(self, response, **kwargs):
        pass

    def video_page_parse(self, response, **kwargs):
        logging.warning("索引页开始爬取！：" + str(response.url))
        # //*[@id="waterfall"]/div
        list_selector = response.xpath("//a[@class='movie-box']")
        for one_selector in list_selector:
            logging.warning("项目信息开始爬取！")
            pageitem = ItemLoader(item=IndexPageItem(), selector=one_selector)
            # //*[@id="waterfall"]/div[1]/a/div[2]/span/date[1]
            pageitem.add_xpath("video_id", "div[@class='photo-info']/span/date[1]/text()")
            # //*[@id="waterfall"]/div[1]/a/div[1]/img
            pageitem.add_xpath("video_title", "div[@class='photo-frame']/img/@title")
            # //*[@id="waterfall"]/div[1]/a
            pageitem.add_xpath("video_url", "@href")
            pageitem.add_xpath("pub_date", "div[@class='photo-info']/span/date[2]/text()")
            pageitem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            logging.warning("项目信息准备提交！：" + pageitem.load_item()["video_id"])
            yield pageitem.load_item()
            logging.warning("项目信息已提交！：" + pageitem.load_item()["video_id"])
            logging.warning("项目信息爬取完毕！")
        logging.warning("索引页爬取完毕！：" + str(response.url))

        logging.warning("详情信息准备压入！：")
        yield Request(url="", callback=self.video_parse, errback=self.parse_err)
        logging.warning("详情信息已压入！：")

        # //*[@id="next"]
        if response.xpath("//*[@id='next']/@href").extract_first() is not None:
            next_url = response.meta["url"] + response.xpath("//*[@id='next']/@href").extract_first()
            logging.warning(msg=str("下一个索引页地址准备压入：" + next_url))
            yield Request(url=next_url, callback=self.video_page_parse, errback=self.parse_err,
                          meta={"url": response.meta["url"]})
            logging.warning(msg=str("下一个索引页地址已压入！：" + next_url))
        else:
            logging.warning("索引页不存在或者到底！:" + str(response.url))

            logging.warning("最新地址列表页开始爬取！")
            # /html/body/div[4]/div/div[2]/div/div
            url_selectors = response.xpath("/html/body/div[4]/div/div[2]/div/div")
            for url_selector in url_selectors:
                logging.warning("最新地址列表项目开始爬取！")
                # /html/body/div[4]/div/div[2]/div/div[1]/a
                latest_url_item = ItemLoader(item=LatestUrlItem(), selector=url_selector)
                latest_url_item.add_xpath("url", "a/text()")
                latest_url_item.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                logging.warning("最新地址列表项目准备提交！:" + latest_url_item.load_item()["url"])
                yield latest_url_item.load_item()
                logging.warning("最新地址列表项目已提交！:" + latest_url_item.load_item()["url"])
                logging.warning("最新地址列表项目爬取完毕！")
            logging.warning("最新地址列表页爬取完毕！")

    def video_parse(self, response, **kwargs):
        # //tr[contains(@class,'result')]
        logging.warning("详情信息页开始爬取！：" + str(response.url))
        # /html/body/div[5]
        list_selector = response.xpath("//div[@class='container']")
        for one_selector in list_selector:
            logging.warning("详情信息项目开始爬取！")
            videoitem = ItemLoader(item=VideoItem(), selector=one_selector)
            videoitem.add_xpath("video_id", "//span[contains(text(),'識別碼:')]/../span[2]/text()")
            videoitem.add_xpath("video_title", "//a[@class='bigImage']/img/@title")
            videoitem.add_xpath("premiered", "//span[contains(text(),'發行日期:')]/../text()")
            videoitem.add_xpath("runtime", "//span[contains(text(),'長度:')]/../text()")
            videoitem.add_xpath("director", "//span[contains(text(),'導演:')]/../a/text()")
            videoitem.add_xpath("studio", "//span[contains(text(),'製作商:')]/../a/text()")
            videoitem.add_xpath("label", "//span[contains(text(),'發行商:')]/../a/text()")
            videoitem.add_xpath("series", "//span[contains(text(),'系列:')]/../a/text()")
            videoitem.add_xpath("bigimg", "//a[@class='bigImage']/@href")
            videoitem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            logging.warning("详情信息项目准备提交！：" + videoitem.load_item()["video_id"])
            yield videoitem.load_item()
            logging.warning("详情信息项目已提交！：" + videoitem.load_item()["video_id"])
            logging.warning("详情信息项目爬取完毕！")
        logging.warning("详情信息页爬取完毕！：" + str(response.url))

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


class JavBusConfig:

    @classmethod
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

    @classmethod
    def get_system_version(self):
        mysystem = platform.platform()
        if mysystem.find("Windows") == 0:
            return "Windows"
        elif mysystem.find("Linux") == 0:
            return "Linux"
        else:
            return "Others"


class MyItemLoader(scrapy.loader.ItemLoader):
    def add_xpath(self, field_name, xpath, *processors, **kw):
        values = self._get_xpathvalues(xpath, **kw)
        if values:
            self.add_value(field_name, values, *processors, **kw)
        else:
            self.add_value(field_name, 'null', *processors, **kw)
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from ..items import PageItem
import time
import browsercookie


class JavdbSpider(Spider):
    name = "javdb"

    # 重写起始函数
    def start_requests(self):
        main_url = "https://javdb36.com/"
        start_urls = [
            main_url + "censored",
            # main_url + "uncensored",
            # main_url + "western",
        ]
        for start_url in start_urls:
            yield Request(url=start_url, callback=self.page_parse)

    # 页面解析函数
    def page_parse(self, response, **kwargs):
        # //*[@id="videos"]/div/div[1]
        list_selector = response.xpath("//*[@id='videos']/div/div")
        for one_selector in list_selector:
            pageitem = ItemLoader(item=PageItem(), selector=one_selector)
            # //*[@id="videos"]/div/div[2]/a/div[2]
            pageitem.add_xpath("video_id", "a/div[@class='uid']/text()")
            pageitem.add_xpath("video_title", "a/div[@class='video-title']/text()")
            # //*[@id="videos"]/div/div[2]/a
            pageitem.add_xpath("video_url", "a/@href")
            pageitem.add_xpath("pub_date", "a/div[@class='meta']/text()")
            # //*[@id="videos"]/div/div[2]/a/div[5]/span[2]
            pageitem.add_xpath("is_today", "a/div[@class='tags has-addons']/span[@class='tag is-info']/text()")
            pageitem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            yield pageitem.load_item()

    # 详情页解析函数
    def detail_parse(self, response, **kwargs):
        pass


if __name__ == "__main__":

    cookiejar = browsercookie.chrome()
    for cookie in cookiejar:
        print(cookie)

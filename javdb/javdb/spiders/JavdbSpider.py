from scrapy import Request
from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from ..items import PageItem
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
        # //*[@id="videos"]/div/div
        list_selector = response.xpath("//*[@id='grid-item']")
        for one_selector in list_selector:
            pageitem = ItemLoader(item=PageItem(), selector=one_selector)
            # //*[@id="videos"]/div/div[1]/a/div[2]

            pageitem.add_xpath("video_id", "a/div[2]")
            yield pageitem.load_item()

    # 详情页解析函数
    def detail_parse(self, response, **kwargs):
        pass


if __name__ == "__main__":

    cookiejar = browsercookie.chrome()
    for cookie in cookiejar:
        print(cookie)

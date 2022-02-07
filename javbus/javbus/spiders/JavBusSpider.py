from scrapy import Request
from scrapy.spiders import Spider
from ..items import VideoPageItem
from scrapy.loader import ItemLoader
import time
import pandas as pd
from sqlalchemy import create_engine


class JavBusSpider(Spider):
    name = "javbus"

    def start_requests(self):
        start_urls = [
            "https://www.busfan.club"
        ]
        for start_url in start_urls:
            yield Request(url=start_url, callback=self.page_parse, meta={"url": start_url})

        video_urls = [

        ]
        for video_url in video_urls:
            yield Request(url=video_url, callback=self.detail_parse)

    def parse(self, response, **kwargs):
        pass

    def page_parse(self, response, **kwargs):
        try:
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
            next_url = response.meta["url"] + response.xpath("//*[@id='next']/@href").extract_first()
            print(next_url)
            yield Request(url=next_url, callback=self.page_parse, meta={"url": response.meta["url"]})
        except TypeError:
            pass
        finally:
            print("索引页面检索完毕。")

    def detail_parse(self, response, **kwargs):
        # //tr[contains(@class,'result')]
        pass

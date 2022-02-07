from scrapy import Request
from scrapy.spiders import Spider
from ..items import VideoPageItem
from scrapy.loader import ItemLoader
import time
import pandas as pd
from sqlalchemy import create_engine
from scrapy.utils.project import get_project_settings


class JavBusSpider(Spider):
    name = "javbus"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None

    def start_requests(self):
        start_urls = [
            "https://www.busfan.club"
        ]
        for start_url in start_urls:
            try:
                yield Request(url=start_url, callback=self.video_page_parse, meta={"url": start_url})
            except TypeError:
                print("起始页面获取错误！")

    def get_detail_requests(self):
        settings = get_project_settings()
        db_name = settings("MYSQL_DB_NAME")
        host = settings("MYSQL_HOST")
        user = settings("MYSQL_USER")
        pwd = settings("MYSQL_PASSWORD")
        self.engine = create_engine(
            str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, pwd, host, db_name)
        )
        sql_query = 'select * from video_page_info;'
        df_read = pd.read_sql_query(sql_query, self.engine)
        print(df_read)

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

        try:
            # //*[@id="next"]
            next_url = response.meta["url"] + response.xpath("//*[@id='next']/@href").extract_first()
            print(next_url)
            yield Request(url=next_url, callback=self.video_page_parse, meta={"url": response.meta["url"]})
        except TypeError:
            print("索引页面获取错误！")
            self.get_detail_requests()

    def detail_parse(self, response, **kwargs):
        # //tr[contains(@class,'result')]
        pass

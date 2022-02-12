import scrapy
from scrapy.loader import ItemLoader
from ..items import VideoItem
from ..items import ActressPageItem
import logging
from ..settings import *
import pandas as pd
from sqlalchemy import create_engine
from .JavBusSpider import JavBusConfig
import time


class VideoPageSpider(scrapy.Spider):
    name = 'video_page'
    custom_settings = {
        "LOG_FILE": "./logs/video_page.log",
        "ITEM_PIPELINES": {
            'javbus.pipelines.VideoPagePipeline': 300,
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.warning("A" * 60)
        logging.warning("VideoPage爬虫开始！")
        db_name = MYSQL_DB_NAME
        if JavBusConfig.get_system_version() == "Windows":
            host = MYSQL_HOST
        else:
            host = "127.0.0.1"
        user = MYSQL_USER
        pwd = MYSQL_PASSWORD
        self.engine = create_engine(
            str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, pwd, host, db_name)
        )
        self.video_id = None

    def __del__(self):
        self.engine.dispose()
        logging.warning("VideoPage爬虫结束！")
        logging.warning("A" * 60)

    def start_requests(self):
        sql_query = 'select * from video_url_spider;'
        df_read = pd.read_sql_query(sql_query, self.engine)
        for video_url in list(df_read["video_url"]):
            yield scrapy.Request(url=video_url, callback=self.parse, errback=JavBusConfig.parse_err)

    def parse(self, response, **kwargs):
        logging.warning("B" * 60)
        logging.warning("详情信息页开始爬取！：" + str(response.url))
        # /html/body/div[5]
        one_selector = response.xpath("//div[@class='container']")
        videoitem = ItemLoader(item=VideoItem(), selector=one_selector)
        videoitem.add_xpath("video_id", "//span[contains(text(),'識別碼:')]/../span[2]/text()")
        videoitem.add_xpath("video_title", "//a[@class='bigImage']/img/@title")
        videoitem.add_value("video_title", "null")
        videoitem.add_xpath("premiered", "//span[contains(text(),'發行日期:')]/../text()")
        videoitem.add_value("premiered", "null")
        videoitem.add_xpath("runtime", "//span[contains(text(),'長度:')]/../text()")
        videoitem.add_value("runtime", "null")
        videoitem.add_xpath("director", "//span[contains(text(),'導演:')]/../a/text()")
        videoitem.add_value("director", "null")
        videoitem.add_xpath("studio", "//span[contains(text(),'製作商:')]/../a/text()")
        videoitem.add_value("studio", "null")
        videoitem.add_xpath("label", "//span[contains(text(),'發行商:')]/../a/text()")
        videoitem.add_value("label", "null")
        videoitem.add_xpath("series", "//span[contains(text(),'系列:')]/../a/text()")
        videoitem.add_value("series", "null")
        videoitem.add_xpath("bigimg", "//a[@class='bigImage']/@href")
        videoitem.add_value("bigimg", "null")
        videoitem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.video_id = videoitem.load_item()["video_id"]
        yield videoitem.load_item()
        # //*[@id="star_sb9"]/li/div
        actress_selectors = response.xpath("//div[@class='star-name']")
        for one_selector in actress_selectors:
            actresspageotem = ItemLoader(item=ActressPageItem(), selector=one_selector)
            actresspageotem.add_value("video_id", self.video_id)
            actresspageotem.add_xpath("actress_url", "a/@href")
            actresspageotem.add_value("actress_url", "null")
            actresspageotem.add_xpath("actress_name", "a/@title")
            actresspageotem.add_value("actress_url", "null")
            actresspageotem.add_value("last_update", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            actresspageotem.load_item()
        logging.warning("详情信息页爬取完毕！：" + str(response.url))
        logging.warning("B" * 60)

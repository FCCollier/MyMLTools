# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


def replace_all(mydata):
    # 去除空格和换行符号
    mydata[0] = str(mydata[0]).strip()
    mydata[0] = str(mydata[0]).replace('\n', '')
    return mydata


class PageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_id = scrapy.Field(input_processor=replace_all, output_processor=TakeFirst())
    video_title = scrapy.Field(input_processor=replace_all, output_processor=TakeFirst())
    video_url = scrapy.Field(input_processor=replace_all, output_processor=TakeFirst())
    # pub_date = scrapy.Field(input_processor=replace_all, output_processor=TakeFirst())
    is_today = scrapy.Field(input_processor=replace_all, output_processor=TakeFirst())
    last_update = scrapy.Field(input_processor=replace_all, output_processor=TakeFirst())

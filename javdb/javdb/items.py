# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_id = scrapy.Field()
    video_title = scrapy.Field()
    video_url = scrapy.Field()
    pub_date = scrapy.Field()
    is_today = scrapy.Field()
    last_update = scrapy.Field()

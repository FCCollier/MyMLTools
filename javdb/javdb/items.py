# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


class IndexpageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_id = scrapy.Field(output_processor=TakeFirst())
    video_title = scrapy.Field(output_processor=TakeFirst())
    video_url = scrapy.Field(output_processor=TakeFirst())
    premiered = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())

import scrapy
from itemloaders.processors import TakeFirst


def replace_all(mydata):
    # 去除空格和换行符号
    mydata[0] = str(mydata[0]).strip()
    mydata[0] = str(mydata[0]).replace('\n', '')
    return mydata


class VideoPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_id = scrapy.Field(output_processor=TakeFirst())
    video_title = scrapy.Field(output_processor=TakeFirst())
    video_url = scrapy.Field(output_processor=TakeFirst())
    pub_date = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())


class VideoItem(scrapy.Item):
    video_id = scrapy.Field(output_processor=TakeFirst())
    video_title = scrapy.Field(output_processor=TakeFirst())
    pub_date = scrapy.Field(output_processor=TakeFirst())
    length = scrapy.Field(output_processor=TakeFirst())
    director = scrapy.Field(output_processor=TakeFirst())
    studio = scrapy.Field(output_processor=TakeFirst())
    label = scrapy.Field(output_processor=TakeFirst())
    series = scrapy.Field(output_processor=TakeFirst())


class ActressItem(scrapy.Item):
    pass


class ActressPageItem(scrapy.Item):
    actress_id = scrapy.Field(output_processor=TakeFirst())
    actress_url = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())
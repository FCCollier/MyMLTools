import scrapy
from itemloaders.processors import TakeFirst, MapCompose


class ProcessItem:
    @classmethod
    def none_process(cls, item):
        pass


class IndexPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_id = scrapy.Field(output_processor=TakeFirst())
    video_title = scrapy.Field(output_processor=TakeFirst())
    video_url = scrapy.Field(output_processor=TakeFirst())
    premiered = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())


class VideoItem(scrapy.Item):
    video_id = scrapy.Field()
    video_title = scrapy.Field()
    premiered = scrapy.Field()
    runtime = scrapy.Field(
        input_processor=MapCompose(str.strip, str.rstrip("分鐘")),
        output_processor=TakeFirst()
    )
    director = scrapy.Field()
    studio = scrapy.Field()
    label = scrapy.Field()
    series = scrapy.Field()
    bigimg = scrapy.Field()
    last_update = scrapy.Field()


class ActressItem(scrapy.Item):
    pass


class ActressPageItem(scrapy.Item):
    actress_id = scrapy.Field(output_processor=TakeFirst())
    actress_url = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())


class LatestUrlItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())

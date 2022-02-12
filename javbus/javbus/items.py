import scrapy
from itemloaders.processors import TakeFirst, MapCompose


class ProcessItem:
    @classmethod
    def none_process(cls, item):
        if item:
            return item
        else:
            return None

    @classmethod
    def runtime_process(cls, item):
        if item:
            return item[0].strip().rstrip("分鐘")
        else:
            return "null"


class IndexPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_id = scrapy.Field(output_processor=TakeFirst())
    video_title = scrapy.Field(output_processor=TakeFirst())
    video_url = scrapy.Field(output_processor=TakeFirst())
    premiered = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())


class VideoItem(scrapy.Item):
    video_id = scrapy.Field(output_processor=TakeFirst())
    video_title = scrapy.Field(output_processor=TakeFirst())
    premiered = scrapy.Field(output_processor=TakeFirst())
    runtime = scrapy.Field(
        input_processor=ProcessItem.runtime_process,
        output_processor=TakeFirst()
    )
    director = scrapy.Field(output_processor=TakeFirst())
    studio = scrapy.Field(output_processor=TakeFirst())
    label = scrapy.Field(output_processor=TakeFirst())
    series = scrapy.Field(output_processor=TakeFirst())
    bigimg = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())


class ActressItem(scrapy.Item):
    pass


class ActressPageItem(scrapy.Item):
    actress_id = scrapy.Field(output_processor=TakeFirst())
    actress_url = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())


class LatestUrlItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    last_update = scrapy.Field(output_processor=TakeFirst())

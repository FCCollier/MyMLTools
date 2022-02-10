import scrapy


class VideoPageSpider(scrapy.Spider):
    name = 'video_page'
    allowed_domains = ['javbus.com']
    start_urls = ['http://javbus.com/']

    def parse(self, response):
        pass

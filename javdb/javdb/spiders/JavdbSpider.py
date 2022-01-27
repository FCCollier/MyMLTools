from scrapy import Request
from scrapy.spiders import Spider


class JavdbSpider(Spider):
    name = "javdb"

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass
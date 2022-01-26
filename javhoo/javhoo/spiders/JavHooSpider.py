from scrapy import Request
from scrapy.spiders import Spider


class JavHooSpider(Spider):
    name = "hot"

    def start_requests(self):
        start_url = ""
        yield Request(start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        pass


if __name__ == "__main__":
    pass
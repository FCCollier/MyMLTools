from scrapy import Request
from scrapy.spiders import Spider


class JavBusSpider(Spider):
    name = "javbus"

    def start_requests(self):
        start_urls = [
            "https://www.busfan.club"
        ]
        for start_url in start_urls:
            yield Request(url=start_url, callback=self.page_parse)

    def page_parse(self, response, **kwargs):
        print(response.status)

    def detail_parse(self, response, **kwargs):
        pass

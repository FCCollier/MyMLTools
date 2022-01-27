from scrapy import Request
from scrapy.spiders import Spider
import browsercookie




class JavdbSpider(Spider):
    name = "javdb"

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass


if __name__ == "__main__":

    cookiejar=browsercookie.chrome()
    for cookie in cookiejar:
        print(cookie)

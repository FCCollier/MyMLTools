from scrapy import cmdline


if __name__ == "__main__":
    cmdline.execute("cd ./javbus".split())
    cmdline.execute("scrapy crawl javbus".split())
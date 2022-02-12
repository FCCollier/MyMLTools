import os


if __name__ == "__main__":
    os.system("scrapy crawl index_page")
    os.system("scrapy crawl video_page")
    os.system("scrapy crawl last_url")
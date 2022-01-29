# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb


class PagePipeline:

    def open_spider(self, spider):
        db_name = spider.settings.get("MYSQL_DB_NAME")
        host = spider.settings.get("MYSQL_HOST")
        user = spider.settings.get("MYSQL_USER")
        pwd = spider.settings.get("MYSQL_PASSWORD")
        self.db_conn = MySQLdb.connect(
            db=db_name,
            host=host,
            user=user,
            password=pwd
        )
        self.db_corsor = self.db_conn.cursor()

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        self.db_conn.close()

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
        values = (
            item["video_id"],
            item["video_title"],
            item["video_url"],
            # item["pub_date"],
            item["is_today"],
            item["last_update"],
        )
        sql = '''
        insert into page_info(video_id,video_title,video_url,is_today,last_update) 
        values(%s,%s,%s,%s,%s)
        '''
        self.db_corsor.execute(sql, values)
        return item

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        self.db_conn.close()

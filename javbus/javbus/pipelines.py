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
            item["pub_date"],
            item["last_update"],
        )
        sql = '''
        insert into video_page_info(video_id,video_title,video_url,pub_date,last_update) 
        values(%s,%s,%s,%s,%s)
        '''
        self.db_corsor.execute(sql, values)
        self.db_conn.commit()
        return item

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        self.db_conn.close()

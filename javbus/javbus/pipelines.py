import mysql.connector
from .settings import *
import logging


class PagePipeline:

    def __init__(self):
        self.db_cursor = None
        self.db_conn = None

    def open_spider(self, spider):
        db_name = MYSQL_DB_NAME
        host = MYSQL_HOST
        user = MYSQL_USER
        pwd = MYSQL_PASSWORD
        self.db_conn = mysql.connector.connect(
            host=host,
            user=user,
            password=pwd,
            database=db_name
        )
        self.db_cursor = self.db_conn.cursor()

    def process_item(self, item, spider):
        try:
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
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
        except mysql.connector.errors.IntegrityError as e:
            values = (
                item["video_title"],
                item["video_url"],
                item["pub_date"],
                item["last_update"],
                item["video_id"],
            )
            sql = ''' 
                    UPDATE video_page_info
                    SET video_title=%s,video_url=%s,pub_date=%s,last_update=%s
                    where video_id=%s
                    '''
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
            logging.info(msg="告警类型：" + str(e))
            logging.info(item["video_id"] + "更新成功！")
        except BaseException as e:
            self.db_conn.rollback()
            logging.warning(msg="错误类型：" + str(e))
        else:
            logging.info(item["video_id"] + "插入成功！")
        return item

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()

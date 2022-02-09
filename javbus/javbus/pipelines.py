import mysql.connector
from .settings import *
from .items import VideoPageItem
from .items import LatestUrlItem
import logging
import platform


class PagePipeline:

    def __init__(self):
        self.db_cursor = None
        self.db_conn = None

    def open_spider(self, spider):
        db_name = MYSQL_DB_NAME
        if self.get_system_version() == "Windows":
            host = MYSQL_HOST
        else:
            host = "127.0.0.1"
        user = MYSQL_USER
        pwd = MYSQL_PASSWORD
        self.db_conn = mysql.connector.connect(
            host=host,
            user=user,
            password=pwd,
            database=db_name
        )
        self.db_cursor = self.db_conn.cursor()
        logging.warning("数据库连接创建完毕，数据库游标创建完毕！")

    def process_item(self, item, spider):
        logging.warning("管道项目处理开始：")
        if isinstance(item, VideoPageItem):
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
                logging.warning(msg="警告信息：" + str(e))
                logging.warning("更新成功！：" + item["video_id"])
            except BaseException as e:
                self.db_conn.rollback()
                logging.error(msg="错误信息：" + str(e))
            else:
                logging.warning("插入成功！：" + item["video_id"])
        elif isinstance(item, LatestUrlItem):
            try:
                values = (
                    item["url"],
                    item["last_update"],
                )
                sql = '''
                        insert into latest_url(url,last_update) 
                        values(%s,%s)
                        '''
                self.db_cursor.execute(sql, values)
                self.db_conn.commit()
            except mysql.connector.errors.IntegrityError as e:
                values = (
                    item["last_update"],
                    item["url"],
                )
                sql = ''' 
                        UPDATE latest_url
                        SET last_update=%s
                        where url=%s
                        '''
                self.db_cursor.execute(sql, values)
                self.db_conn.commit()
                logging.warning(msg="警告信息：" + str(e))
                logging.warning("更新成功！：" + item["url"])
            except BaseException as e:
                self.db_conn.rollback()
                logging.error(msg="错误信息：" + str(e))
            else:
                logging.warning("插入成功！：" + item["url"])
        else:
            logging.warning("未找到对应的Item类！")
        logging.warning("管道项目处理结束。")
        return item

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()
        logging.warning("数据库游标关闭，数据库连接关闭！")

    def get_system_version(self):
        mysystem = platform.platform()
        if mysystem.find("Windows") == 0:
            return "Windows"
        elif mysystem.find("Linux") == 0:
            return "Linux"
        else:
            return "Others"

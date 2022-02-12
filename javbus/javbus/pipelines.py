import mysql.connector
from .settings import *
from .items import IndexPageItem
from .items import VideoItem
from .items import LatestUrlItem
import logging
from .spiders.JavBusSpider import JavBusConfig


class PagePipeline:

    def __init__(self):
        self.db_cursor = None
        self.db_conn = None

    def open_spider(self, spider):
        db_name = MYSQL_DB_NAME
        if JavBusConfig.get_system_version() == "Windows":
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
        logging.warning("数据库连接创建完毕，数据库游标创建完毕！数据库地址：" + str(host))

    def process_item(self, item, spider):
        logging.warning("管道项目处理开始：")
        if isinstance(item, IndexPageItem):
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
        elif isinstance(item, VideoItem):
            try:
                values = (
                    item["video_id"],
                    item["video_title"],
                    item["premiered"],
                    item["runtime"],
                    item["director"],
                    item["studio"],
                    item["label"],
                    item["series"],
                    item["bigimg"],
                    item["last_update"],
                )
                sql = '''
                        insert into video_info(video_id,video_title,premiered,runtime,director,studio,label,series,bigimg,last_update) 
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
                self.db_cursor.execute(sql, values)
                self.db_conn.commit()
            except mysql.connector.errors.IntegrityError as e:
                logging.warning(msg="警告信息：" + str(e))
                logging.warning("更新成功！：" + item["video_id"])
            else:
                logging.warning("插入成功！：" + item["video_id"])
        else:
            logging.warning("未找到对应的Item类！")
        logging.warning("管道项目处理结束。")
        return item

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()
        logging.warning("数据库游标关闭，数据库连接关闭！")


class IndexPagePipeline:
    def __init__(self):
        self.db_cursor = None
        self.db_conn = None

    def open_spider(self, spider):
        db_name = MYSQL_DB_NAME
        if JavBusConfig.get_system_version() == "Windows":
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
        logging.warning("C" * 60)
        logging.warning("数据库连接创建完毕，数据库游标创建完毕！数据库地址：" + str(host))

    def process_item(self, item, spider):
        try:
            values = (
                item["video_id"],
                item["video_title"],
                item["video_url"],
                item["premiered"],
                item["last_update"],
            )
            sql = '''
            insert into video_page_info(video_id,video_title,video_url,premiered,last_update) 
            values(%s,%s,%s,%s,%s)
            '''
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
        except mysql.connector.errors.IntegrityError as e:
            values = (
                item["video_title"],
                item["video_url"],
                item["premiered"],
                item["last_update"],
                item["video_id"],
            )
            sql = ''' 
            UPDATE video_page_info
            SET video_title=%s,video_url=%s,premiered=%s,last_update=%s
            where video_id=%s
            '''
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
            logging.warning("更新成功！：" + item["video_id"])
        except BaseException as e:
            self.db_conn.rollback()
            logging.error(msg="错误信息：" + str(e))
        else:
            logging.warning("插入成功！：" + item["video_id"])

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()
        logging.warning("数据库游标关闭，数据库连接关闭！")
        logging.warning("C" * 60)


class VideoPagePipeline:
    def __init__(self):
        self.db_cursor = None
        self.db_conn = None

    def open_spider(self, spider):
        db_name = MYSQL_DB_NAME
        if JavBusConfig.get_system_version() == "Windows":
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
        logging.warning("C" * 60)
        logging.warning("数据库连接创建完毕，数据库游标创建完毕！数据库地址：" + str(host))

    def process_item(self, item, spider):
        item = MyDataProcess.none_process(item)
        try:
            values = (
                item["video_id"],
                item["video_title"],
                item["premiered"],
                item["runtime"],
                item["director"],
                item["studio"],
                item["label"],
                item["series"],
                item["bigimg"],
                item["last_update"],
            )
            sql = '''
            insert into video_info(video_id,video_title,premiered,runtime,director,studio,label,series,bigimg,last_update) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
        except mysql.connector.errors.IntegrityError as e:
            values = (
                item["video_title"],
                item["premiered"],
                item["runtime"],
                item["director"],
                item["studio"],
                item["label"],
                item["series"],
                item["bigimg"],
                item["last_update"],
                item["video_id"],
            )
            sql = '''
            UPDATE video_info
            SET video_title=%s,premiered=%s,runtime=%s,director=%s,studio=%s,label=%s,series=%s,bigimg=%s,last_update=%s
            where video_id=%s
            '''
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
            logging.warning(msg="警告信息：" + str(e))
            logging.warning("更新成功！：" + item["video_id"])
        else:
            logging.warning("插入成功！：" + item["video_id"])

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()
        logging.warning("数据库游标关闭，数据库连接关闭！")


class LastUrlPipeline:
    def __init__(self):
        self.db_cursor = None
        self.db_conn = None

    def open_spider(self, spider):
        db_name = MYSQL_DB_NAME
        if JavBusConfig.get_system_version() == "Windows":
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
        logging.warning("C" * 60)
        logging.warning("数据库连接创建完毕，数据库游标创建完毕！数据库地址：" + str(host))

    def process_item(self, item, spider):
        item = MyDataProcess.none_process(item)
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

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()
        logging.warning("数据库游标关闭，数据库连接关闭！")


class MyDataProcess:
    @classmethod
    def none_process(cls, item):
        try:
            for key in item:
                if item[key] == "null":
                    item[key] = None
            return item
        except BaseException as e:
            logging.error("错误类型：" + str(e))
            return None

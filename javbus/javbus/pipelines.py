import pandas as pd
from sqlalchemy import create_engine


class PagePipeline:

    def __init__(self):
        self.engine = None

    def open_spider(self, spider):
        db_name = spider.settings.get("MYSQL_DB_NAME")
        host = spider.settings.get("MYSQL_HOST")
        user = spider.settings.get("MYSQL_USER")
        pwd = spider.settings.get("MYSQL_PASSWORD")
        self.engine = create_engine(
            str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, pwd, host, db_name)
        )

    def process_item(self, item, spider):
        try:
            df_write = pd.DataFrame(
                {
                    'video_id': [item["video_id"]],
                    'video_title': [item["video_title"]],
                    'video_url': [item["video_url"]],
                    'pub_date': [item["pub_date"]],
                    'last_update': [item["last_update"]]
                }
            )
            df_write.to_sql(
                name='video_page_info',
                con=self.engine,
                index=False,
                if_exists="append"
            )
        except KeyError as e:
            print('键值错误：', e, '\n')
        else:
            print('其他类型错误')
        finally:
            pass

        return item

    def close_spider(self, spider):
        self.engine.dispose()

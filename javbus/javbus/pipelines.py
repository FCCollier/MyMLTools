import pandas as pd
from sqlalchemy import create_engine
from scrapy.utils.project import get_project_settings


class PagePipeline:

    def __init__(self):
        self.engine = None

    def open_spider(self, spider):
        settings = get_project_settings()
        db_name = settings("MYSQL_DB_NAME")
        host = settings("MYSQL_HOST")
        user = settings("MYSQL_USER")
        pwd = settings("MYSQL_PASSWORD")
        self.engine = create_engine(
            str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, pwd, host, db_name)
        )

    def process_item(self, item, spider):
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
        return item

    def close_spider(self, spider):
        self.engine.dispose()

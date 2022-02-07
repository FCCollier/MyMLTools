import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://myscrapy:ReAwVFYtePgkSQcI@82.157.160.44:3306/javbus')
# sql_query = 'select * from video_page_info;'
# df_read = pd.read_sql_query(sql_query, engine)
# print(df_read)
df_write = pd.DataFrame(
    {
        'video_id': ['111'],
        'video_title': ['111'],
        'video_url': ['111'],
        'pub_date': ['2021-01-01'],
        'last_update': ['2021-01-01 00:00:00']
    }
)
df_write.to_sql('video_page_info', con=engine, index=False, if_exists="append")
engine.dispose()

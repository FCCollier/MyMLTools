import pandas as pd
from sqlalchemy import create_engine

host = "82.157.160.44"
user = "myscrapy"
password = "ReAwVFYtePgkSQcI"
database = "javbus"

engine = create_engine(
    str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, password, host, database)
)

sql_query = 'select * from video_url_spider;'
df_read = pd.read_sql_query(sql_query, engine)

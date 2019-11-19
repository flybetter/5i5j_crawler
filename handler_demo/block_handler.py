import time
import stomp
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import traceback
from pandas.io.json import json_normalize
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import os

mysql_df = None


def save(df):
    engine = create_engine(
        py_targe_mysql,
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )

    df.to_sql('crawl_block_compare', con=engine, if_exists='append', index=False)


def compare(tmp_df):
    blockName = tmp_df.loc[0, 'blockName']
    filter_df = filter_blockName(blockName)
    if len(filter_df) > 0:
        tmp_df['local_block_id'] = filter_df.loc[filter_df.index.values[0], 'local_block_id']
        tmp_df['local_block_name'] = filter_df.loc[filter_df.index.values[0], 'local_block_name']
    return tmp_df


def filter_blockName(blockName):
    filter_df = mysql_df[mysql_df['local_block_name'] == blockName]
    return filter_df


def mysql_df():
    global mysql_df
    sql = "select id as local_block_id  ,blockname as local_block_name from block"
    engine = create_engine(
        py_offical_mysql,
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    df = pd.read_sql(sql=sql, con=engine)
    mysql_df = df


class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        try:
            df = json_normalize(json.loads(message))
            save_df = compare(df)
            save(save_df)
        except:
            print(traceback.print_exc())


def get_config():
    global py_offical_mysql
    global py_targe_mysql
    py_offical_mysql = os.getenv('PY_OFFICAL_MYSQL')
    py_targe_mysql = os.getenv('PY_TARGE_MYSQL')


def begin():
    mysql_df()
    conn = stomp.Connection10([('localhost', 61613)], auto_content_length=False)
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/block_compare', ack=1)
    time.sleep(60 * 60 * 20)
    conn.disconnect()


if __name__ == '__main__':
    timez = pytz.timezone('Asia/Shanghai')
    scheduler = BlockingScheduler(timezone=timez)
    scheduler.add_executor('processpool')
    scheduler.add_job(begin, 'cron', hour=23, minute=20, second=00, misfire_grace_time=30)
    scheduler.start()
    # begin()

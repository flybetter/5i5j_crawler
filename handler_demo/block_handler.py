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

mysql_df = None


def save(df):
    engine = create_engine(
        "mysql+pymysql://root:idontcare@192.168.105.106/house_developcenter?charset=utf8",
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )

    df.to_sql('sell_compare', con=engine, if_exists='append', index=False)


def custom(df, temp):
    area_parameter = np.maximum(35 - np.abs(df['buildarea'] - temp.loc[0, 'buildArea']) / 2 * 0.1 * 35, 0)

    model_parameter = np.maximum(30 - np.abs(df['room'] - temp.loc[0, 'roomCount']) * 0.5 * 30, 0)

    price_parameter = np.maximum(20 - np.abs(df['price'] - temp.loc[0, 'totalPrice']) * 0.1 * 20, 0)

    list = range(df['totalfloor'])

    divide = round(df['totalfloor'] / 3)

    sub_lists = [list[i:i + divide] for i in range(df['totalfloor']) if i % divide == 0]

    floor_parameter = 0

    for i, v in enumerate(sub_lists):
        if df['floor'] in v:
            if i + 1 == temp.loc[0, 'floorCode']:
                floor_parameter = 15

    df['percent'] = round(area_parameter + model_parameter + price_parameter + floor_parameter)
    return df


def compare(tmp_df):
    blockName = tmp_df.loc[0, 'blockName']
    filter_df = filter_blockName(blockName)
    if len(filter_df) > 0:
        filter_df = filter_df.apply(custom, args=(tmp_df,), axis=1)
        filter_df = filter_df.reset_index()
        target = filter_df.iloc[filter_df['percent'].idxmax()]
        tmp_df['percent'] = target['percent']
        tmp_df['official_id'] = target['id']
    return tmp_df


def filter_blockName(blockName):
    filter_df = mysql_df[mysql_df['blockshowname'] == blockName]
    return filter_df


def mysql_df():
    global mysql_df
    sql = "select id ,blockname from block"
    engine = create_engine(
        "mysql+pymysql://root:idontcare@202.102.74.70/house?charset=utf8",
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
            df['buildArea'] = pd.to_numeric(df['buildArea'])
            save_df = compare(df)
            save(save_df)
        except:
            print(traceback.print_exc())


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

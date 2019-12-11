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


def save_sell(df):
    engine = create_engine(
        py_target_mysql,
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    df.to_sql('crawl_sell_compare', con=engine, if_exists='append', index=False)
    id = pd.read_sql_query('select ifnull(max(id),0) from crawl_sell_compare', con=engine).iloc[0, 0]
    return id


def save_relation(df):
    if df is not None:
        engine = create_engine(
            py_target_mysql,
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )
        df.to_sql('crawl_relation', con=engine, if_exists='append', index=False)


def custom(df, temp):
    area_parameter = np.maximum(35 - np.abs(df['buildarea'] - temp.loc[0, 'buildArea']) / 2 * 0.1 * 35, 0)

    model_parameter = np.maximum(30 - np.abs(df['room'] - temp.loc[0, 'roomCount']) * 0.5 * 30, 0)

    price_parameter = np.maximum(20 - np.abs(df['price'] - temp.loc[0, 'totalPrice']) / (df['price'] * 0.01) * 0.1 * 20,
                                 0)

    floor_parameter = 0

    try:
        rate = df['floor'] / df['totalfloor']
        if rate < 0.334:
            temp_floor_code = 1
        elif rate < 0.667:
            temp_floor_code = 2
        else:
            temp_floor_code = 3

        if temp.loc[0, 'floorCode'] == temp_floor_code:
            floor_parameter = 15
    except:
        pass

    df['percent'] = round(area_parameter + model_parameter + price_parameter + floor_parameter)
    return df


def top5(tmp_df):
    blockName = tmp_df.loc[0, 'blockName']
    filter_df = filter_blockName(blockName)
    if len(filter_df) > 0:
        filter_df = filter_df.apply(custom, args=(tmp_df,), axis=1)
        target = filter_df.sort_values(['percent'], ascending=False)
        target = target.head(5)
        return target
    else:
        return None


def save_all(tmp_df, target):
    if target is not None:
        tmp_target = target.reset_index()
        object = tmp_target.iloc[tmp_target['percent'].idxmax()]
        tmp_df['percent'] = object['percent']
        tmp_df['official_id'] = object['official_id']
        id = save_sell(tmp_df)
        target['crawl_id'] = id
        save_relation(target)
    else:
        save_sell(tmp_df)


def compare(tmp_df, target_id):
    blockName = tmp_df.loc[0, 'blockName']
    filter_df = filter_blockName(blockName)
    if len(filter_df) > 0:
        filter_df = filter_df.apply(custom, args=(tmp_df,), axis=1)
        target = filter_df.sort_values(['percent'], ascending=False)
        target = target.head(5)
        target['crawl_id'] = target_id
        return target
    else:
        return None


def filter_blockName(blockName):
    filter_df = mysql_df[mysql_df['blockshowname'] == blockName]
    return filter_df


def mysql_df():
    global mysql_df
    sql = "select id as official_id,district,address,blockshowname,buildarea,floor,totalfloor,price,averprice,room,blockid,forward,streetid  from sell where  esta=1"
    engine = create_engine(
        py_offical_mysql,
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    mysql_df = pd.read_sql(sql=sql, con=engine)


class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        try:
            df = json_normalize(json.loads(message))
            df['buildArea'] = pd.to_numeric(df['buildArea'])
            target = top5(df)
            save_all(df, target)
            # time.sleep(1)
        except:
            print(traceback.print_exc())


def get_config():
    global py_offical_mysql
    global py_target_mysql
    py_offical_mysql = os.getenv('PY_OFFICAL_MYSQL')
    py_target_mysql = os.getenv('PY_TARGET_MYSQL')


def begin():
    get_config()
    mysql_df()
    conn = stomp.Connection10([('localhost', 61613)], auto_content_length=False)
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/handler', ack=1)
    time.sleep(60 * 60 * 20)
    conn.disconnect()


if __name__ == '__main__':
    timez = pytz.timezone('Asia/Shanghai')
    scheduler = BlockingScheduler(timezone=timez)
    scheduler.add_executor('processpool')
    scheduler.add_job(begin, 'cron', hour=23, minute=20, second=00, misfire_grace_time=30)
    scheduler.start()
    # begin()

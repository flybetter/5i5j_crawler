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
from datetime import datetime
from datetime import timedelta


def get_crawl_data():
    timez = pytz.timezone('Asia/Shanghai')
    now = datetime.now(timez)
    yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    sql = "select id as repeatIds, cityCode,platformId,houseId,url,title,district,subDistrict,blockName,blockId,totalPrice,unitPrice,roomCount,hallCount,toiletCount,totalFloor,floorCode,forward,decoration,buildArea,buildYear,propertyRightYear,listTime,hasLift from  crawl_sell_compare where  date_format(create_time,'%%Y-%%m-%%d %%H:%%i') >'{} 23:25'".format(
        yesterday)
    engine = create_engine(
        py_target_mysql,
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    df = pd.read_sql(sql=sql, con=engine)
    return df


def save_filter_data(df):
    engine = create_engine(
        py_target_mysql,
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    df.to_sql('crawl_filter', con=engine, if_exists='append', index=False)


def duplicate_function(df):
    if len(df['repeatIds']) > 1:
        df['crawlId'] = df['repeatIds'][0]
        df['repeatIds'] = ",".join(map(str, df['repeatIds'][1:]))
    else:
        df['crawlId'] = df['repeatIds'][0]
        df['repeatIds'] = ''

    return df


def duplicate_remove(df):
    data = df.groupby(['blockName', 'totalPrice', 'buildArea', 'roomCount', 'floorCode'])['repeatIds'].apply(
        list).reset_index()
    data = data.apply(duplicate_function, axis=1)
    return data


def filter(df, value):
    return np.abs(df['buildArea'] - value) > 2


def similarity_fuction(df):
    df = df.sort_values('platformId')
    if len(df) > 1:
        for index, row in df.iterrows():
            tmp = df[df.index != index].copy()
            if index in df.index.values:
                tmp.loc[:, 'tagged'] = tmp.apply(filter, args=(row.loc['buildArea'],), axis=1)
                df.loc[index, 'similarIds'] = ",".join(
                    map(str, tmp[tmp['tagged'] == False].loc[:, 'crawlId'].values))
                df.drop(tmp[tmp['tagged'] == False].index.values, inplace=True)

    return df


def similarity_exclusion(df, data):
    df = pd.merge(df, data[['repeatIds', 'platformId']], how='left', left_on='crawlId', right_on='repeatIds')
    df = df.drop(columns='repeatIds_y')
    df.rename(columns={'repeatIds_x': 'repeatIds'}, inplace=True)
    df['similarIds'] = ''

    data = pd.DataFrame(columns=df.columns.tolist())

    for name, group in df.groupby('blockName'):
        data = data.append(similarity_fuction(group), sort=False)
    return data


def get_config():
    global py_offical_mysql
    global py_target_mysql
    py_offical_mysql = os.getenv('PY_OFFICAL_MYSQL')
    py_target_mysql = os.getenv('PY_TARGET_MYSQL')


def begin():
    get_config()
    crawl_data = get_crawl_data()
    filter_data_1 = duplicate_remove(crawl_data)
    result = similarity_exclusion(filter_data_1, crawl_data)
    save_filter_data(result)


if __name__ == '__main__':
    timez = pytz.timezone('Asia/Shanghai')
    scheduler = BlockingScheduler(timezone=timez)
    scheduler.add_executor('processpool')
    scheduler.add_job(begin, 'cron', hour=1, minute=00, second=00, misfire_grace_time=30)
    scheduler.start()
    # begin()

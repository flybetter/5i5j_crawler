import time
import sys
import stomp
from handler_demo.Handler import key_value

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import json


class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)
        print(key_value)

    def on_message(self, headers, message):
        print('received a message %s' % message)


def get_mysql():
    sql = "select * from sell limit 100"
    engine = create_engine(
        "mysql+pymysql://root:idontcare@192.168.105.106/house_developcenter?charset=utf8",
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    df = pd.read_sql(sql=sql, con=engine)
    return df


def test_block_compare(body):
    conn = stomp.Connection10([('192.168.10.109', 61613)])
    conn.connect()
    conn.send(
        body=body,
        destination='/queue/block_compare')
    time.sleep(2)
    conn.disconnect()


def test_block_compare(body):
    conn = stomp.Connection10([('192.168.10.109', 61613)])
    conn.connect()
    conn.send(
        body=body,
        destination='/queue/handler')
    time.sleep(2)
    conn.disconnect()


def block_test():
    # sql = "select *  from crawl_sell_compare where id=21169;"
    sql = "select cityCode,platformId,houseId,url,title,district,subDistrict,blockName,blockId,totalPrice,unitPrice,roomCount,hallCount,toiletCount,totalFloor,floorCode,forward,decoration,buildArea,buildYear,propertyRightYear,listTime,hasLift from     crawl_sell_compare where  date_format(create_time,'%%Y-%%m-%%d') ='2019-12-10'"
    engine = create_engine(
        "mysql+pymysql://root:idontcare@202.102.74.70/house?charset=utf8",
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    df = pd.read_sql(sql=sql, con=engine)
    return df


def send(json):
    conn = stomp.Connection10([('192.168.10.221', 61613)])
    conn.connect()
    conn.send(
        body=json,
        destination='/queue/handler')
    # time.sleep(1)
    conn.disconnect()


def demo2():
    df = block_test()
    datas = df.to_json(orient='records')
    objects = json.loads(datas)
    conn = stomp.Connection10([('192.168.10.109', 61613)])
    conn.connect()
    for object in objects:
        # test_block_compare(json.dumps(object, ensure_ascii=False))
        # print(json.dumps(object, ensure_ascii=False)
        conn.send(
            body=json.dumps(object, ensure_ascii=False),
            destination='/queue/handler')
    conn.disconnect()


if __name__ == '__main__':
    # df = block_test()
    # datas = df.to_json(orient='records')
    # objects = json.loads(datas)
    # for object in objects:
    #     # test_block_compare(json.dumps(object, ensure_ascii=False))
    #     # print(json.dumps(object, ensure_ascii=False)
    #     send(json.dumps(object, ensure_ascii=False))
    demo2()

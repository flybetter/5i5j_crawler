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


def test():
    conn = stomp.Connection10([('192.168.10.109', 61613)])
    conn.connect()
    conn.send(
        body='{"blockId": "277100", "blockName": "德盈国际广场", "buildArea": "37", "buildYear": 0, "cityCode": "nj","decoration": "中装", "district": "雨花台", "floorCode": 2, "forward": "东", "hallCount": 1, "hasLift": 0,"houseId": "43344050", "id": 0, "listTime": "20191022", "platformId": 5, "propertyRightYear": 0, "roomCount": 1,"subDistrict": "能仁里", "title": "德盈国际 精装单室套 中间楼层 采光好", "toiletCount": 0, "totalFloor": 29, "totalPrice": 118.0,"unitPrice": 31900.0, "url": "https://nj.5i5j.com/ershoufang/43344050.html"}',
        destination='/queue/handler')
    time.sleep(2)
    conn.disconnect()


if __name__ == '__main__':
    df = get_mysql()
    datas = df.to_json(orient='records')
    objects = json.loads(datas)
    for object in objects:
        print(json.dumps(object, ensure_ascii=False))

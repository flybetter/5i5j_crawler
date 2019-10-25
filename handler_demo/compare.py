import pandas as pd

from sqlalchemy import create_engine

import numpy as np

from pandas.io.json import json_normalize

import json
import traceback


# {"blockId": "275777", "blockName": "雨花西路", "buildArea": "57", "buildYear": 0, "cityCode": "nj", "decoration": "简装",
#  "district": "雨花台", "floorCode": 3, "forward": "南北", "hallCount": 1, "hasLift": 0, "houseId": "43185189", "id": 0,
#  "listTime": "20191022", "platformId": 5, "propertyRightYear": 0, "roomCount": 3, "subDistrict": "能仁里",
#  "title": "中华门 雨花西路206号 两房出售 实小雨中中间楼层", "toiletCount": 0, "totalFloor": 6, "totalPrice": 192.0,
#  "unitPrice": 33700.0, "url": "https://nj.5i5j.com/ershoufang/43185189.html"}
# {"blockId": "406471", "blockName": "金域中央商业", "buildArea": "2342.9", "buildYear": 0, "cityCode": "nj",
#  "decoration": "简装", "district": "鼓楼", "floorCode": 1, "forward": "北", "hallCount": 1, "hasLift": 0,
#  "houseId": "43639310", "id": 0, "listTime": "20191022", "platformId": 5, "propertyRightYear": 0, "roomCount": 1,
#  "subDistrict": "五塘广场", "title": "五塘广场 幕府西路 金域中央 商业大平层", "toiletCount": 0, "totalFloor": 15, "totalPrice": 7263.0,
#  "unitPrice": 31000.0, "url": "https://nj.5i5j.com/ershoufang/43639310.html"}
# {"blockId": "277100", "blockName": "德盈国际广场", "buildArea": "37", "buildYear": 0, "cityCode": "nj",
#  "decoration": "中装", "district": "雨花台", "floorCode": 2, "forward": "东", "hallCount": 1, "hasLift": 0,
#  "houseId": "43344050", "id": 0, "listTime": "20191022", "platformId": 5, "propertyRightYear": 0, "roomCount": 1,
#  "subDistrict": "能仁里", "title": "德盈国际 精装单室套 中间楼层 采光好", "toiletCount": 0, "totalFloor": 29, "totalPrice": 118.0,
#  "unitPrice": 31900.0, "url": "https://nj.5i5j.com/ershoufang/43344050.html"}


def save(df):
    try:
        engine = create_engine(
            "mysql+pymysql://root:idontcare@192.168.105.106/house_developcenter?charset=utf8",
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )

        df.to_sql('sell_compare', con=engine, if_exists='append', index=False)
    except:
        print(traceback.print_exc())


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

    return round(area_parameter + model_parameter + price_parameter + floor_parameter)


def compare(mysql_df, tmp_df):
    blockName = tmp_df.loc[0, 'blockName']
    filter_df = filter_blockName(mysql_df, blockName)
    if len(filter_df) > 0:
        filter_df['percent'] = filter_df.apply(custom, args=(tmp_df,), axis=1)
        target = filter_df.iloc[filter_df['percent'].idxmax()]
        tmp_df['percent'] = target['percent']
        tmp_df['official_id'] = target['id']
    return tmp_df


def filter_blockName(mysql_df, blockName):
    filter_df = mysql_df[mysql_df['blockshowname'] == blockName]
    return filter_df


if __name__ == '__main__':
    sql = "select id,district,address,blockshowname,buildarea,floor,totalfloor,price,averprice,room from sell where is_real_house=1 and  blockshowname='德盈国际广场'"
    engine = create_engine(
        "mysql+pymysql://root:idontcare@202.102.74.70/house?charset=utf8",
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    mysql_df = pd.read_sql(sql=sql, con=engine)

    message = '{"blockId": "277100", "blockName": "德盈国际广场", "buildArea": "37", "buildYear": 0, "cityCode": "nj","decoration": "中装", "district": "雨花台", "floorCode": 2, "forward": "东", "hallCount": 1, "hasLift": 0,"houseId": "43344050", "id": 0, "listTime": "20191022", "platformId": 5, "propertyRightYear": 0, "roomCount": 1,"subDistrict": "能仁里", "title": "德盈国际 精装单室套 中间楼层 采光好", "toiletCount": 0, "totalFloor": 29, "totalPrice": 118.0,"unitPrice": 31900.0, "url": "https://nj.5i5j.com/ershoufang/43344050.html"}'

    df = json_normalize(json.loads(message))
    df['buildArea'] = pd.to_numeric(df['buildArea'])
    save_df = compare(mysql_df, df)
    save(save_df)

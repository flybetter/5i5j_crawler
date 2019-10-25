import pandas as pd
from pandas.io.json import json_normalize
import json
from sqlalchemy import create_engine

message = '{"blockId": "275777", "blockName": "雨花西路", "buildArea": "57", "buildYear": 0, "cityCode": "nj", "decoration": "简装", "district": "雨花台", "floorCode": 3, "forward": "南北", "hallCount": 1, "hasLift": 0, "houseId": "43185189", "id": 0, "listTime": "20191022", "platformId": 5, "propertyRightYear": 0, "roomCount": 3, "subDistrict": "能仁里", "title": "中华门 雨花西路206号 两房出售 实小雨中中间楼层", "toiletCount": 0, "totalFloor": 6, "totalPrice": 192.0, "unitPrice": 33700.0, "url": "https://nj.5i5j.com/ershoufang/43185189.html"}'

# tmp_df = pd.read_json(message, orient='records')
engine = create_engine(
    "mysql+pymysql://root:idontcare@192.168.105.106/house_developcenter?charset=utf8",
    max_overflow=0,
    pool_size=5,
    pool_timeout=30,
    pool_recycle=-1
)

df = json_normalize(json.loads(message))

print(df['buildArea'].values)

# tmp_df.to_sql('sell_compare', con=engine, if_exists='append', index=False)

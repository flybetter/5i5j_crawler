from sqlalchemy import create_engine
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import stomp

key_value = "11"


class HouseHandler(object):

    def __init__(self):
        self.sql = "select id,district,address,blockshowname,buildarea,floor,totalfloor,price,averprice,room from sell where is_real_house=1"
        self.engine = create_engine(
            "mysql+pymysql://root:idontcare@202.102.74.70/house?charset=utf8",
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )
        self.mysql_df = self.get_mysql_data()

    def get_mysql_data(self):
        print("get the latest data")
        df = pd.read_sql(sql=self.sql, con=self.engine)
        print("over")
        return df

    def on_error(self, headers, message):
        print('received an error %s' % message)
        key_value

    def on_message(self, headers, message):
        print('received a message %s' % message)

    def compare(self):
        pass

    def save(self):
        pass

    def begin(self):
        pass


if __name__ == '__main__':
    pass

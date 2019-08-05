from selenium import webdriver

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import re

from datetime import datetime

import json

import logging

import traceback

from functools import wraps

from sqlalchemy import exc

import urllib3

from selenium.common.exceptions import NoSuchElementException

import time

from selenium.webdriver.chrome.options import Options

option = webdriver.ChromeOptions()

import sys


# 安居客

# 贝壳

# 赶集网


# 1.标题(单间出租)二号线集庆门大街佳和园苏宁慧谷越洋国际可短租月付万
# 2. 价格 950
# 3.付款的方式 押一付一
# 4.户型1室1厅1卫
# 5.装修情况 精装修
# 6.合租的方式整租
# 7.发布时间07 - 27
# 8.面积50㎡
# 9.联系人名称
# 10.houseid
# 11.描述 - -
# 12.url - -
# 13.platform_id
# 14.个人房源
# 15.朝向


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(traceback.print_exc())
            raise e

    return wrapper


class Crawler(object):

    def __init__(self):
        engine = create_engine(
            "mysql+pymysql://root:idontcare@192.168.10.221/demo?charset=utf8",
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )
        SessionFactory = sessionmaker(bind=engine)
        self.session = SessionFactory()

        option.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:67.0) Gecko/20100101 Firefox/67.0"')
        # option.setPageLoadStrategy(PageLoadStrategy.NONE)

        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 2
            }
        }
        # option.add_argument(' blink-settings=imagesEnabled=false')
        #
        # option.add_argument("--disable-javascript")

        option.add_experimental_option('prefs', prefs)

        self.browser = webdriver.Chrome(options=option)

        self.browser.implicitly_wait(10)
        self.browser.set_page_load_timeout(10)

        self.next_url = None

    def action(self):
        self.ganji_action()

    def ganji_action(self):
        self.next_url = "http://nj.ganji.com/zufang/pn9/?key=佳和园"
        # link = "http://nj.ganji.com/zufang/38937057428249x.shtml"

        while self.next_url is not None:
            links = self.ganji_list()
            for link in links:

                flag = True
                for i in range(3):
                    try:
                        self.ganji_data(link)
                        flag = True
                        break
                    except exc.IntegrityError:
                        break
                    except:
                        time.sleep(2)
                        self.proxy()
                        flag = False

                if not flag:
                    print("still not work:" + link)

    def ganji_list(self):

        self.browser.get(self.next_url)

        matcher = re.search("(\\d+)/", self.next_url)

        if matcher.group(1) is not None:
            num = int(matcher.group(1)) + 1

            if num is 29:
                sys.exit()
            self.next_url = re.sub('\\d+/', str(num) + '/', self.next_url)
            print(self.next_url)

        divs = self.browser.find_elements_by_xpath("//dt[@class='img']/div[@class='img-wrap']/a")

        if divs is None:
            self.browser.quit()
            self.session.close()

        return filter(lambda x: "fanggongyu" not in str(x), [div.get_attribute("href") for div in divs])
        # return [div.get_attribute("href") for div in divs]

    # @retry(stop_max_attempt_number=3)
    @decorator
    def ganji_data(self, url):
        print(url)
        print(self.next_url)
        self.browser.get(url)

        if "firewall" in self.browser.current_url:
            raise Exception("firwall")

        body = dict()

        body["id"] = 0
        body["platform_id"] = 1
        body["house_id"] = re.search("zufang/(\\d+x).shtml", self.browser.current_url).group(1)
        body["url"] = self.browser.current_url
        body["title"] = self.browser.find_element_by_class_name("card-title").text
        body["price"] = self.browser.find_element_by_class_name("price").text
        houseStruct = self.browser.find_elements_by_class_name("content")[0].text
        counts = re.split('[\u4e00-\u9fa5]', houseStruct)
        body["room_count"] = counts[0]
        body["hall_count"] = counts[1]
        body["toilet_count"] = counts[2]
        body["forward"] = self.browser.find_elements_by_class_name("content")[2].text
        body["decoration"] = self.browser.find_elements_by_class_name("content")[4].text
        detail = self.browser.find_elements_by_class_name("content")[1].text
        details = re.split('  ', detail)
        body["area"] = float(str(details[1]).replace('㎡', "").strip())
        body["pay_way"] = self.browser.find_element_by_class_name('unit').text
        body["create_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body["share_way"] = details[0]
        body["public_time"] = self.browser.find_element_by_class_name("date").text
        body["linkman"] = self.browser.find_element_by_xpath("//div[@class='name']/a").text
        body["description"] = self.browser.find_element_by_xpath("//div[@class='describe']/div").text

        if "女士" in body["linkman"] or "先生" in body["linkman"] or "小姐" in body["linkman"]:
            body["source"] = 1
        else:
            body["source"] = 2

        body["phone"] = self.browser.find_element_by_class_name("phone_num").text

        print(json.dumps(body, ensure_ascii=False))

        # placeholders = ',:'.join(body.keys())
        # columns = ', '.join(body.keys())
        # sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('rent', columns, placeholders)
        # print(sql)
        # sql2="INSERT INTO sell_5i5j ( floorCode, totalPrice, platformId, blockId, roomCount, decoration, listTime, totalFloor, toiletCount, id, district, title, hasLift, forward, cityCode, blockName, subDistrict, buildArea, unitPrice, propertyRightYear, houseId, url, buildYear, hallCount ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )" % ( list( body.values()))
        # print(sql2)
        self.session.execute(
            "INSERT INTO rent ( id, platform_id, house_id, url, title, price, room_count, hall_count, toilet_count, forward, decoration, area, pay_way, create_date, share_way, public_time, linkman, description, source ,phone) VALUES ( id,:platform_id,:house_id,:url,:title,:price,:room_count,:hall_count,:toilet_count,:forward,:decoration,:area,:pay_way,:create_date,:share_way,:public_time,:linkman,:description,:source,:phone )",
            body)

        self.session.commit()

    def save(self):
        pass

    def proxy(self):
        url = 'http://api.ip.data5u.com/dynamic/get.html?order=1e0fba269c82476195e5df6329007cea&ttl=1&json=1&sep=3'
        http = urllib3.PoolManager()
        # 通过request()方法创建一个请求：
        r = http.request('GET', url)
        object = json.loads(r.data.decode())

        self.browser.quit()

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument(
            '--proxy-server=http://' + str(object["data"][0]["ip"]) + ':' + str(object["data"][0]["port"]) + '')
        chromeOptions.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:67.0) Gecko/20100101 Firefox/67.0"')
        # option.setPageLoadStrategy(PageLoadStrategy.NONE)

        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 2
            }
        }
        # option.add_argument(' blink-settings=imagesEnabled=false')
        #
        # option.add_argument("--disable-javascript")

        chromeOptions.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(options=chromeOptions)
        self.browser.implicitly_wait(10)
        self.browser.set_page_load_timeout(10)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.action()

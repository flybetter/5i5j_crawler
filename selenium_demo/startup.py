# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from selenium import webdriver
from sqlalchemy.orm import sessionmaker

import logging
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECss

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import json

import stomp

from functools import wraps

import traceback

from datetime import datetime

import logging

import sys
import os

from sqlalchemy import create_engine

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(filename=os.path.join(os.getcwd(), "log.txt"), level=logging.INFO)


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(traceback.print_exc())

    return wrapper


class BrowserEngine(object):

    def __init__(self, url="https://nj.5i5j.com/ershoufang/n1/"):
        # chromeOptions.add_argument("--proxy-server=http://117.60.10.29:35787")
        # chromeOptions.add_argument(
        #     'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        # chromeOptions.add_argument(
        #     'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:67.0) Gecko/20100101 Firefox/67.0"')
        capa = DesiredCapabilities.FIREFOX
        capa["pageLoadStrategy"] = "eager"
        # capa["pageLoadStrategy"] = "normal"
        location = "C:\Program Files\Mozilla Firefox/firefox.exe"
        self.browser = webdriver.Firefox(firefox_binary=location, desired_capabilities=capa)
        self.next_page = url
        # self.links = list()
        # self.conn = stomp.Connection10([('192.168.10.221', 61613)], auto_content_length=False)
        #         # self.conn.start()
        #         # self.conn.connect()

        engine = create_engine(
            "mysql+pymysql://root:idontcare@192.168.105.106/house_developcenter?charset=utf8",
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )
        SessionFactory = sessionmaker(bind=engine)
        self.session = SessionFactory()

    def action(self):
        while self.next_page is not None:
            self.check_next_page()
            self.get_links()

        self.session.close()

    def get_links(self):
        items = WebDriverWait(self.browser, 10).until(
            lambda x: x.find_elements_by_xpath("//div[@class='listImg']/a[@target='_blank']"))
        # items = self.browser.find_elements_by_xpath("//div[@class='listImg']/a[@target='_blank']")

        links = [item.get_attribute("href") for item in items]

        for link in links:
            self.get_data(link)

    @decorator
    def get_data(self, url):

        body = dict()

        logging.info(url)
        print(url)

        starttime = datetime.now()

        self.browser.get(url)

        city_code = "nj"

        body['city_code'] = city_code

        platform_id = 5

        body['platform_id'] = platform_id

        body['url'] = url

        houseId = re.search("(\\d+).html", self.browser.current_url).group(1)

        body['house_id'] = houseId

        title = WebDriverWait(self.browser, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "house-tit")))

        # title = self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/h1").text

        body['title'] = title.text

        district = str(self.browser.find_element_by_xpath("/html/body/div[2]/div/div[1]/a[3]").text).replace("二手房", "")
        body['district'] = district

        sub_district = str(self.browser.find_element_by_xpath("/html/body/div[2]/div/div[1]/a[4]").text).replace("二手房",
                                                                                                                 "")
        body['sub_district'] = sub_district

        block_name = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[1]/a").text

        body['block_name'] = block_name

        block_id = re.search("(\\d+).html", self.browser.find_element_by_xpath(
            "/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[1]/a").get_attribute("href")).group(1)

        body['block_id'] = block_id

        total_price = float(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div/p[1]").text)

        body['total_price'] = total_price

        unit_price = float(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/p[1]").text) * 10000

        body['unit_price'] = unit_price

        floors = str(self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[2]").text).split(
            "/")

        total_floor = floors[1].replace("层", "")

        body['total_floor'] = int(total_floor)

        if "低" in floors[0] or '底' in floors[0]:
            floor_code = 1
        elif "中" in floors[0]:
            floor_code = 2

        elif "高" in floors[0] or '顶' in floors[0]:
            floor_code = 3

        body['floor_code'] = floor_code

        forward = str(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[3]").text).replace("朝向：\n",
                                                                                                                "")

        body['forward'] = forward

        decoration = str(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[4]").text).replace("装修：\n",
                                                                                                                "")

        body['decoration'] = decoration

        build_area = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[4]/div/p[1]").text

        body['build_area'] = build_area
        print(str(self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[6]").text).replace(
            "年代：\n", "").replace("年", ""))
        try:
            build_year = int(
                str(self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[6]").text).replace(
                    "年代：\n", "").replace("年", ""))
        except Exception as e:
            build_year = 0

        body['build_year'] = build_year

        has_lift = 0

        body['has_lift'] = has_lift

        property_right_year = 0

        body['property_right_year'] = property_right_year

        houseStruct = self.browser.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[3]/div[1]/div/div[2]/ul/li[1]/span").text

        counts = re.split('[\u4e00-\u9fa5]', houseStruct)

        room_count = counts[0]

        body['room_count'] = int(room_count)

        hall_count = counts[1]

        body['hall_count'] = int(hall_count)

        toilet_count = counts[2]

        body['toilet_count'] = int(toilet_count)

        list_time = str(self.browser.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[3]/div[1]/div/div[2]/ul/li[5]/span").text).replace("-", "")

        body['list_time'] = list_time

        body['id'] = 0

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body['create_date'] = dt
        body['update_date'] = dt

        msg = json.dumps(body, sort_keys=True, ensure_ascii=False)

        logging.info(msg)

        print(msg)

        # placeholders = ',:'.join(body.keys())
        # columns = ', '.join(body.keys())
        # sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('sell_5i5j', columns, placeholders)
        # print(sql)
        # sql2="INSERT INTO sell_5i5j ( floorCode, totalPrice, platformId, blockId, roomCount, decoration, listTime, totalFloor, toiletCount, id, district, title, hasLift, forward, cityCode, blockName, subDistrict, buildArea, unitPrice, propertyRightYear, houseId, url, buildYear, hallCount ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )" % ( list( body.values()))
        # print(sql2)
        try:
            self.session.execute(
                "INSERT INTO sell_5i5j ( floor_code, total_floor, decoration, room_count, toilet_count, id, district, title, hall_count, unit_price, forward, city_code, block_id, build_year, build_area, total_price, house_id, url, has_lift, property_right_year, platform_id, block_name, sub_district, list_time,create_date,update_date ) VALUES ( :floor_code,:total_floor,:decoration,:room_count,:toilet_count,:id,:district,:title,:hall_count,:unit_price,:forward,:city_code,:block_id,:build_year,:build_area,:total_price,:house_id,:url,:has_lift,:property_right_year,:platform_id,:block_name,:sub_district,:list_time,:create_date,:update_date )",
                body)

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
        endtime = datetime.now()
        logging.info(str((endtime - starttime).seconds))
        print(str((endtime - starttime).seconds))

    def check_next_page(self):
        logging.info(self.next_page)
        print("next Page:" + self.next_page)
        self.browser.get(self.next_page)

        mather = re.search('n(\\d+)', self.next_page)

        # logging.info(mather.group(1))

        if mather.group(1) is not None:
            num = int(mather.group(1)) + 1
            self.next_page = re.sub('n(\\d+)', 'n' + str(num), self.next_page)

        # try:
        #     self.browser.find_element_by_css_selector('li.nodata ')
        #     # self.browser.close()
        # except Exception as e:
        #     pass


# def send():
#     browser = webdriver.Chrome()
#     browser.get('https://nj.5i5j.com/ershoufang/43183776.html')
#     browser.get('https://nj.5i5j.com/ershoufang/n10000/')
#     browser.implicitly_wait(100)
#
#
# def Pager():
#     passss


if __name__ == '__main__':
    demo = BrowserEngine(url="https://nj.5i5j.com/ershoufang/n47/")
    demo.action()

    # msg = "我爱你中文"
    # conn = stomp.Connection10([('192.168.105.105', 61613)], auto_content_length=False)
    # conn.start()
    # conn.connect()
    # conn.send(destination="/queue/SellHouseQueue", body=msg)
    # conn.disconnect()

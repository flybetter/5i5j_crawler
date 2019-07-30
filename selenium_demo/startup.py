# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from selenium import webdriver
import logging
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import json

import stomp

from functools import wraps

import traceback

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

chromeOptions = webdriver.ChromeOptions()


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            traceback.print_exc()

    return wrapper

class BrowserEngine(object):

    def __init__(self, url="https://nj.5i5j.com/ershoufang/n1/"):
        # chromeOptions.add_argument("--proxy-server=http://117.60.10.29:35787")
        # chromeOptions.add_argument(
        #     'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        chromeOptions.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:67.0) Gecko/20100101 Firefox/67.0"')

        self.browser = webdriver.Chrome(options=chromeOptions)
        self.next_page = url
        # self.links = list()
        self.conn = stomp.Connection10([('192.168.10.221', 61613)], auto_content_length=False)
        self.conn.start()
        self.conn.connect()

    def action(self):
        while self.next_page is not None:
            self.check_next_page()
            self.get_links()

        self.conn.disconnect()

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

        print(url)

        self.browser.get(url)

        city_code = "nj"

        body['cityCode'] = city_code

        platform_id = 5

        body['platformId'] = platform_id

        body['url'] = url

        houseId = re.search("(\\d+).html", self.browser.current_url).group(1)

        body['houseId'] = houseId

        title = self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/h1").text

        body['title'] = title

        district = str(self.browser.find_element_by_xpath("/html/body/div[2]/div/div[1]/a[3]").text).replace("二手房", "")
        body['district'] = district

        sub_district = str(self.browser.find_element_by_xpath("/html/body/div[2]/div/div[1]/a[4]").text).replace("二手房",
                                                                                                                 "")
        body['subDistrict'] = sub_district

        block_name = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[1]/a").text

        body['blockName'] = block_name

        block_id = re.search("(\\d+).html", self.browser.find_element_by_xpath(
            "/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[1]/a").get_attribute("href")).group(1)

        body['blockId'] = block_id

        total_price = float(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div/p[1]").text)

        body['totalPrice'] = total_price

        unit_price = float(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/p[1]").text) * 10000

        body['unitPrice'] = unit_price

        floors = str(self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[2]").text).split(
            "/")

        body['subDistrict'] = sub_district

        total_floor = floors[1].replace("层", "")

        body['totalFloor'] = int(total_floor)

        if "低" in floors[0] or '底' in floors[0]:
            floor_code = 1
        elif "中" in floors[0]:
            floor_code = 2

        elif "高" in floors[0] or '顶' in floors[0]:
            floor_code = 3

        body['floorCode'] = floor_code

        forward = str(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[3]").text).replace("朝向：\n",
                                                                                                                "")

        body['forward'] = forward

        decoration = str(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[4]").text).replace("装修：\n",
                                                                                                                "")

        body['decoration'] = decoration

        build_area = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[4]/div/p[1]").text

        body['buildArea'] = build_area

        build_year = int(str(
            self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[6]").text).replace("年代：\n",
                                                                                                                "").replace(
            "年", ""))
        body['buildYear'] = build_year

        has_lift = 0

        body['hasLift'] = has_lift

        property_right_year = 0

        body['propertyRightYear'] = property_right_year

        houseStruct = self.browser.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[3]/div[1]/div/div[2]/ul/li[1]/span").text

        body['subDistrict'] = sub_district

        counts = re.split('[\u4e00-\u9fa5]', houseStruct)

        room_count = counts[0]

        body['roomCount'] = int(room_count)

        hall_count = counts[1]

        body['hallCount'] = int(hall_count)

        toliet_count = counts[2]

        body['toiletCount'] = int(toliet_count)

        list_time = str(self.browser.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[3]/div[1]/div/div[2]/ul/li[5]/span").text).replace("-", "")

        body['listTime'] = list_time

        body['id'] = 0

        msg = json.dumps(body, sort_keys=True, ensure_ascii=False)

        print(msg)

        self.conn.send("SellHouseQueue", msg)



    def check_next_page(self):
        self.browser.get(self.next_page)

        mather = re.search('n(\\d+)', self.next_page)

        # print(mather.group(1))

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
#     pass


if __name__ == '__main__':
    demo = BrowserEngine(url="https://nj.5i5j.com/ershoufang/n1/")
    demo.action()

    # msg = "我爱你中文"
    # conn = stomp.Connection10([('192.168.105.105', 61613)], auto_content_length=False)
    # conn.start()
    # conn.connect()
    # conn.send(destination="/queue/SellHouseQueue", body=msg)
    # conn.disconnect()

from selenium import webdriver
import logging
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import queue
from selenium.webdriver.common.keys import Keys

import json

import traceback

from functools import wraps

import stomp
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

# https://nj.5i5j.com/ershoufang/n100/

chromeOptions = webdriver.ChromeOptions()


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.info(traceback.print_exc())
            print(traceback.print_exc())

    return wrapper


class BrowserEngine(object):

    def __init__(self, url="https://nj.5i5j.com/ershoufang/n1/"):
        # chromeOptions.add_argument("--proxy-server=http://117.60.10.29:35787")
        # chromeOptions.add_argument(
        #     'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        # chromeOptions.add_argument(
        #     'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:67.0) Gecko/20100101 Firefox/67.0"')
        # chrome_options = webdriver.ChromeOptions()
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chromeOptions)
        self.next_page = url
        # self.links = list()
        self.conn = stomp.Connection10([('192.168.10.221', 61613)], auto_content_length=False)
        self.conn.start()
        self.conn.connect()

    def action(self):
        while self.check_next_latest_page():
            self.get_links()

        self.browser.quit()
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

        self.browser.get(url)

        city_code = "nj"

        body['cityCode'] = city_code

        platform_id = 5

        body['platformId'] = platform_id

        body['url'] = url

        houseId = re.search("(\\d+).html", self.browser.current_url).group(1)

        body['houseId'] = houseId

        title = self.browser.find_element_by_class_name("house-tit").text

        body['title'] = title

        district = str(self.browser.find_element_by_xpath("//div[@class='zushous']/ul/li[3]/a[1]").text).replace("二手房",
                                                                                                                 "")

        body['district'] = district

        sub_district = str(self.browser.find_element_by_xpath("//div[@class='zushous']/ul/li[3]/a[2]").text).replace(
            "二手房",
            "")

        body['subDistrict'] = sub_district

        block_name = self.browser.find_element_by_xpath("//div[@class='zushous']/ul/li[1]/a").text

        body['blockName'] = block_name

        block_id = re.search("(\\d+).html", self.browser.find_element_by_xpath(
            "//div[@class='zushous']/ul/li[1]/a").get_attribute("href")).group(1)

        body['blockId'] = block_id

        total_price = float(
            self.browser.find_element_by_xpath("//div[@class='de-price fl']/span").text)

        body['totalPrice'] = total_price

        unit_price = round(float(
            self.browser.find_element_by_xpath("//div[@class='danjia']/span").text) * 10000, 2)

        body['unitPrice'] = unit_price

        # for text in self.browser.find_elements_by_xpath("//p[@class='houseinfor2']"):
        #     print(text.text)

        floors = str(self.browser.find_element_by_xpath("//p[@class='houseinfor2'][1]").text).split(
            "/")

        total_floor = floors[1].replace("层", "")

        body['totalFloor'] = int(total_floor)

        if "低" in floors[0] or '底' in floors[0]:
            floor_code = 1
        elif "中" in floors[0]:
            floor_code = 2

        elif "高" in floors[0] or '顶' in floors[0]:
            floor_code = 3

        body['floorCode'] = floor_code

        forward = str(self.browser.find_elements_by_xpath("//p[@class='houseinfor1']")[2].text)

        body['forward'] = forward

        decoration = str(self.browser.find_elements_by_xpath("//p[@class='houseinfor2']")[1].text)

        body['decoration'] = decoration

        build_area = str(self.browser.find_elements_by_xpath("//p[@class='houseinfor1']")[1].text).replace("m²", "")

        body['buildArea'] = build_area

        try:
            build_year = int(str(
                self.browser.find_element_by_xpath("//div[@class='infocon fl']/ul/li[4]/span").text).replace("年代：\n",
                                                                                                             "").replace(
                "年", ""))
        except Exception as e:
            build_year = 0

        body['buildYear'] = build_year

        has_lift = 0

        body['hasLift'] = has_lift

        property_right_year = 0

        body['propertyRightYear'] = property_right_year

        houseStruct = self.browser.find_element_by_xpath(
            "//div[@class='infocon fl']/ul/li[1]/span").text

        counts = re.split('[\u4e00-\u9fa5]', houseStruct)

        room_count = counts[0]

        body['roomCount'] = int(room_count)

        hall_count = counts[1]

        body['hallCount'] = int(hall_count)

        if len(counts) == 3:
            toliet_count = counts[2]
            body['toiletCount'] = int(toliet_count)
        else:
            body['toiletCount'] = 0

        list_time = str(self.browser.find_element_by_xpath(
            "//div[@class='infocon fl']/ul/li[3]/span").text).replace("-", "")

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

    def check_next_latest_page(self):
        self.browser.get(self.next_page)
        items = WebDriverWait(self.browser, 10).until(
            lambda x: x.find_elements_by_xpath("//div[@class='listX']/p[3]"))

        flag_result = False
        for item in items:
            if "今天发布" in item.text:
                flag_result = True
                break

        if flag_result:
            mather = re.search('n(\\d+)', self.next_page)
            num = int(mather.group(1)) + 1
            self.next_page = re.sub('n(\\d+)', 'n' + str(num), self.next_page)
            return True
        else:
            return False


def begin():
    demo = BrowserEngine(url="https://nj.5i5j.com/ershoufang/o8n1/")
    demo.action()


if __name__ == '__main__':

    timez = pytz.timezone('Asia/Shanghai')
    scheduler = BlockingScheduler(timezone=timez)
    scheduler.add_executor('processpool')
    scheduler.add_job(begin, 'cron', hour=23, minute=00, second=00, misfire_grace_time=30)
    # scheduler.start()
    begin()

    # msg = "我爱你中文"
    # conn = stomp.Connection10([('192.168.105.105', 61613)], auto_content_length=False)
    # conn.start()
    # conn.connect()
    # conn.send(destination="/queue/SellHouseQueue", body=msg)
    # conn.disconnect()

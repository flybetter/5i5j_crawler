from selenium import webdriver

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import re

from datetime import datetime

import json


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
        self.browser = webdriver.Chrome()
        self.next_url = None

    def action(self):
        self.ganji_action()

    def ganji_action(self):
        self.next_url = "http://nj.ganji.com/zufang/pn1/?key=佳和园"

        while self.next_url is not None:
            links = self.ganji_list()
            for link in links:
                self.ganji_data(link)

    def ganji_list(self):
        self.browser.get(self.next_url)

        matcher = re.search("(\\d+)", self.next_url)

        if matcher.group(1) is None:
            num = int(matcher.group(1)) + 1
            self.next_page = re.sub('(\\d+)', num, self.next_page)

        divs = self.browser.find_elements_by_xpath("//dt[@class='img']/div[@class='img-wrap']/a")

        return [div.get_attribute("href") for div in divs]

    def ganji_data(self, url):
        self.browser.get(url)

        body = dict()

        body["id"] = 0
        body["platform_id"] = 1
        body["house_id"] = re.search("zufang/(\\d+x).shtml", self.browser.current_url).group(1)
        body["url"] = self.browser.current_url
        body["title"] = self.browser.find_element_by_class_name("card-title").text
        body["price"] = self.browser.find_element_by_class_name("price").text
        houseStruct = self.browser.find_element_by_xpath(
            "//ul[@class='er-list f-clear']/li[@class='item f-fl'][0]/span[@class='content']").text
        counts = re.split('[\u4e00-\u9fa5]', houseStruct)
        body["room_count"] = counts[0]
        body["hall_count"] = counts[1]
        body["toilet_count"] = counts[2]
        body["forward"] = self.browser.find_element_by_xpath(
            "//ul[@class='er-list f-clear']/li[@class='item f-fl'][2]/span[@class='content']").text
        body["decoration"] = self.browser.find_element_by_xpath(
            "//ul[@class='er-list f-clear']/li[@class='item f-fl'][4]/span[@class='content']").text

        detail = self.browser.find_element_by_xpath(
            "//ul[@class='er-list f-clear']/li[@class='item f-fl'][1]/span[@class='content']").text
        details = re.split('\s', detail)

        body["area"] = float(str(details[1]).replace('㎡', ""))
        body["pay_way"] = self.browser.find_element_by_class_name('unit')
        body["create_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body["share_way"] = details[0]
        body["public_time"] = self.browser.find_element_by_class_name("date").text
        body["linkman"] = self.browser.find_element_by_xpath("//div[@class='name']/a").text
        body["description"] = self.browser.find_element_by_class_name("item").text

        if "女生" in body["linkman"] or "男士" in body["linkman"] or "小姐" in body["linkman"]:
            body["source"] = 1
        else:
            body["source"] = 2

        print(json.dumps(body, ensure_ascii=False, ))

    def save(self):
        pass


if __name__ == '__main__':
    crawler = Crawler()
    crawler.action()

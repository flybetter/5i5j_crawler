from selenium import webdriver
import logging
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import queue

# https://nj.5i5j.com/ershoufang/n100/

chromeOptions = webdriver.ChromeOptions()


class BrowserEngine(object):

    def __init__(self, url="https://nj.5i5j.com/ershoufang/n1/"):
        # chromeOptions.add_argument("--proxy-server=http://117.60.10.29:35787")
        # chromeOptions.add_argument(
        #     'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        chromeOptions.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:67.0) Gecko/20100101 Firefox/67.0"')

        self.browser = webdriver.Chrome(options=chromeOptions)
        self.next_page = url
        self.links = list()

    def action(self):
        self.check_next_page()
        self.get_links()

    def get_links(self):
        items = self.browser.find_elements_by_xpath("//ul[@class='zhbcont']/li/a[@target='_blank']")
        for item in items:
            href = item.get_attribute("href")
            self.links.append("")

    def get_data(self, url):
        print(self.browser.get(url))

    def check_next_page(self):
        self.browser.get(self.next_page)

        mather = re.search('n(\\d+)', self.next_page)

        print(mather.group(1))

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
    demo = BrowserEngine(url="https://nj.5i5j.com/ershoufang/n100/")
    demo.action()

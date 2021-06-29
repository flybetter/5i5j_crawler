from selenium import webdriver



def chrome_function(url):
    browser = webdriver.Chrome()
    browser.get(url)
    print(browser.page_source)
    browser.close()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.implicitly_wait(2)
    browser.get("http://nj.ke.com/ershoufang/103102654878.html?fb_expo_id=462181816624578560")
    divs = browser.find_elements_by_xpath("//div[@class='item mytime']")
    result = list()
    for div in divs:
        result.append(div.text)
    browser.close()

import urllib.request
import urllib.parse
from lxml.html import parse
from lxml import etree
import json
from pandas.io.json import json_normalize
import re
import pandas as pd
from selenium import webdriver
import datetime


def read_csv():
    df = pd.read_csv("demo.csv")
    return df['actionUrl'].to_list()


def url_action(url):
    print(url)
    browser = webdriver.Chrome()
    browser.get(url)
    divs = browser.find_elements_by_xpath("//div[@class='item mytime']")
    result_demo = []
    for div in divs:
        result_demo.append(div.text)

    count = browser.find_elements_by_xpath("//span[@class='count']")[0].text
    browser.close()
    return result_demo, count


def save_csv(df, results, stars_list):
    s = pd.Series(results)
    df_times = pd.DataFrame(s)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    df_times.columns = ['detail_times_' + date]
    df_times['times' + date] = df_times['detail_times_' + date].map(lambda x: len(x))
    df_final = pd.concat([df, df_times], axis=1)

    s_1 = pd.Series(stars_list)
    df_stars = pd.DataFrame(s_1)
    df_stars.columns = ['starts_' + date]
    df_final = pd.concat([df_final, df_stars], axis=1)

    df_final.to_csv("demo2.csv")


if __name__ == '__main__':
    results = list()
    stars_list = list()
    df = pd.read_csv("demo.csv")
    list = df['actionUrl'].to_list()
    for i, url in enumerate(list):
        print(i)
        result_list, start_count = url_action(url)
        results.append(result_list)
        stars_list.append(start_count)

    save_csv(df, results, stars_list)




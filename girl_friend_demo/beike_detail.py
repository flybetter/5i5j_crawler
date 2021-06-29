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
    browser.close()
    return result_demo


def save_csv(df, results):
    s = pd.Series(results)
    df_times = pd.DataFrame(s)
    date=datetime.datetime.strftime('%Y-%m-%d')
    df_times.columns = ['detail_times'+date]
    df_times['times'+date] = df_times['detail_times'+date].map(lambda x: len(x))
    df_final = pd.concat([df, df_times], axis=1)
    df_final.to_csv("demo2.csv")


if __name__ == '__main__':
    results = list()
    df = pd.read_csv("demo.csv")
    list = df['actionUrl'].to_list()
    for i, url in enumerate(list):
        print(i)
        results.append(url_action(url))
    save_csv(df, results)

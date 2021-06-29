import urllib.request
import urllib.parse
from lxml.html import parse
from lxml import etree
import json
from pandas.io.json import json_normalize
import re
import pandas as pd

def read_csv():
    df = pd.read_csv("demo.csv")
    return df['actionUrl'].to_list()


def url_action(url):
    url_http = url.replace('https', 'http')
    print(url_http)
    response = urllib.request.urlopen(url_http)
    print(response.read().decode('utf-8'))


if __name__ == '__main__':
    # list = read_csv()
    # for url in list:
    #     url_action(url)

    url = "http://nj.ke.com/ershoufang/103102654878.html?fb_expo_id=462181816624578560"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(url=request)
    print(response.read().decode('utf-8'))


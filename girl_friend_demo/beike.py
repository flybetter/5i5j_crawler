import urllib.request
import urllib.parse
from lxml.html import parse
from lxml import etree
import json
from pandas.io.json import json_normalize
import re


def data_print(source):
    # print(source['data']['list'])
    df = json_normalize(source['data']['list'])
    print(df)
    df.to_csv("demo.csv")
    # for object in source['data']['list']:
    #     print(object)
    # df = json_normalize(json.dumps(source['data']['list'], ensure_ascii=False))
    # df.to_csv("demo.csv")


def save_function(results):
    df = json_normalize(results)
    df.to_csv("demo.csv")


def url_action(num):
    url = "http://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/drawhouselist?cityId=320100&dataSource=ESF&curPage=2&condition=l3bp0ep210&resblockIds=1411045966153,1411000000039,1411000000613,1411000000670,1411000000807,1411000000853,1411000000065,1411000000293,1411000000506,1411000000557,1411000000007,1411000000064,1411000000135,1411000000476,1411000000699,1411000000707,1411000000814,1411000000816,1411000000862,1411042945603,1411047634823,1411000000005,1411000000010,1411000000011,1411000000091,1411000000213,1411000000413,1411000000441,1411000000467,1411000000496,1411000000516,1411000000780,1411000000901,1411041183926,1411041748814,1411042956541,1411043492179,1411062302233".format(str(num))
    response = urllib.request.urlopen(url)
    print(url)
    print(json.dumps(json.loads(response.read().decode('utf-8')), ensure_ascii=False))
    source = json.loads(response.read().decode('utf-8'))
    return source['data']['list']


if __name__ == '__main__':
    results = list()
    for i in range(1, 5):
        results.extend(url_action(i))

    print(len(results))
    save_function(results)

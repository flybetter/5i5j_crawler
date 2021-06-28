import urllib.request
import urllib.parse
from lxml.html import parse
from lxml import etree

import re


def demo():
    values = ['010000', '010100', '010200', '010400', '010500', '010600', '011100', '011300', '011400', '011500',
              '011600', '011700',
              '011800', '012300']

    # values = ['010200']

    names = ['南京市秦淮区－区人民法院',
             '南京市六合区－市公安局六合分局',
             '南京市玄武区－区市场监督管理局',
             '南京市栖霞区－区科学技术局',
             '南京市江宁区－区市场监督管理局',
             '南京市溧水区－区市场监督管理局',
             '南京市－市商务局',
             '南京市－市文化和旅游局',
             '南京市鼓楼区－团区委',
             '南京市江宁区－区财政局',
             '南京市六合区－竹镇镇人民政府',
             '南京市－浦口监狱',
             '南京市－江宁监狱']

    name_dict = {'南京市秦淮区－区人民法院': 1,
                 '南京市六合区－市公安局六合分局': 3,
                 '南京市玄武区－区市场监督管理局': 3,
                 '南京市栖霞区－区科学技术局': 1,
                 '南京市江宁区－区市场监督管理局': 2,
                 '南京市溧水区－区市场监督管理局': 5,
                 '南京市－市商务局': 3,  # 两年
                 '南京市－市文化和旅游局': 3,  # 两年
                 '南京市鼓楼区－团区委': 1,
                 '南京市江宁区－区财政局': 2,
                 '南京市六合区－竹镇镇人民政府': 2,
                 '南京市－浦口监狱': 3,
                 '南京市－江宁监狱': 3
                 }

    flag_name = dict()

    for key in values:
        # 定义一个字典参数
        data_dict = dict()
        data_dict['jobAreaList'] = key
        # 使用urlencode将字典参数序列化成字符串
        data_string = urllib.parse.urlencode(data_dict)
        # 将序列化后的字符串转换成二进制数据，因为post请求携带的是二进制参数
        last_data = bytes(data_string, encoding='utf-8')
        # 如果给urlopen这个函数传递了data这个参数，那么它的请求方式则不是get请求，而是post请求
        response = urllib.request.urlopen("http://218.94.85.11:8000/Home/RegBrowse?examid=00201009105751",
                                          data=last_data)
        # 我们的参数出现在form表单中，这表明是模拟了表单的提交方式，以post方式传输数据
        # print(response.read().decode('utf-8'))
        data = response.read().decode('utf-8')
        html = etree.HTML(data)
        results = html.xpath('//td/text()')
        i = 0
        for demo in results:
            name = str(re.sub(r'\[\d+\]', '', demo.strip()))
            if name.strip() in names:
                if name.strip() in flag_name.keys():
                    flag_name[name.strip()] = flag_name[name.strip()] + 1
                else:
                    flag_name[name.strip()] = 1
                if flag_name[name.strip()] == name_dict[name.strip()]:
                    i = 5

            if i > 0:
                print(re.sub(r'\[\d+\]', '', demo.strip()))
                i = i - 1


def demo2():
    values = ['010000', '010100', '010200', '010400', '010500', '010600', '011100', '011300', '011400', '011500',
              '011600', '011700',
              '011800', '012300']

    names = ['南京市秦淮区－区人民法院',
             '南京市六合区－市公安局六合分局',
             '南京市玄武区－区市场监督管理局',
             '南京市栖霞区－区科学技术局',
             '南京市江宁区－区市场监督管理局',
             '南京市溧水区－区市场监督管理局',
             '南京市－市商务局',
             '南京市－市文化和旅游局',
             '南京市鼓楼区－团区委',
             '南京市江宁区－区财政局',
             '南京市六合区－竹镇镇人民政府',
             '南京市－浦口监狱',
             '南京市－江宁监狱']

    name_dict = {'南京市秦淮区－区人民法院': 1,
                 '南京市六合区－市公安局六合分局': 3,
                 '南京市玄武区－区市场监督管理局': 3,
                 '南京市栖霞区－区科学技术局': 1,
                 '南京市江宁区－区市场监督管理局': 2,
                 '南京市溧水区－区市场监督管理局': 5,
                 '南京市－市商务局': 3,  # 两年
                 '南京市－市文化和旅游局': 3,  # 两年
                 '南京市鼓楼区－团区委': 1,
                 '南京市江宁区－区财政局': 2,
                 '南京市六合区－竹镇镇人民政府': 2,
                 '南京市－浦口监狱': 3,
                 '南京市－江宁监狱': 3
                 }

    street = set()

    for key in values:
        # 定义一个字典参数
        data_dict = dict()
        data_dict['jobAreaList'] = key
        # 使用urlencode将字典参数序列化成字符串
        data_string = urllib.parse.urlencode(data_dict)
        # 将序列化后的字符串转换成二进制数据，因为post请求携带的是二进制参数
        last_data = bytes(data_string, encoding='utf-8')
        # 如果给urlopen这个函数传递了data这个参数，那么它的请求方式则不是get请求，而是post请求
        response = urllib.request.urlopen("http://218.94.85.11:8000/Home/RegBrowse?examid=00201009105751",
                                          data=last_data)
        # 我们的参数出现在form表单中，这表明是模拟了表单的提交方式，以post方式传输数据
        # print(response.read().decode('utf-8'))
        data = response.read().decode('utf-8')
        html = etree.HTML(data)
        results = html.xpath('//td/text()')
        i = 0
        for demo in results:
            name = str(re.sub(r'\[\d+\]', '', demo.strip()))
            if '街道' in name.strip():
                street.add(name.strip())
                i = 5

            if i > 0:
                print(re.sub(r'\[\d+\]', '', demo.strip()))
                i = i - 1

        # for value in street:
        #     print(value)


# 测试网址：http://httpbin.org/post
if __name__ == '__main__':
    demo()
    # names = ['南京市秦淮区－区人民法院',
    #          '南京市六合区－市公安局六合分局',
    #          '南京市玄武区－区市场监督管理局',
    #          '南京市栖霞区－区科学技术局',
    #          '南京市江宁区－区市场监督管理局',
    #          '南京市溧水区－区市场监督管理局',
    #          '南京市－市商务局',
    #          '南京市－市文化和旅游局',
    #          '南京市鼓楼区－团区委',
    #          '南京市江宁区－区财政局',
    #          '南京市六合区－竹镇镇人民政府']
    #
    # name = '南京市秦淮区－区人民法院'
    #
    # print(name in names)

    # parsed = parse(response)
    # doc = parsed.getroot()
    # 找到html中有<table></table>的所有table，以列表的形式返回给tables
    # tables = doc.findall('.//table')
    # 我们要的是第一个table
    # content = tables[0].text_content()
    # print(content)
    # tds = tables[0].findall('.//tr')
    # for td in tds:
    #     print(td.text_content())

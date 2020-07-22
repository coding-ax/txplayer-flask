# -*- coding:utf-8 -*-
# @Time : 2020/7/9 20:39
# @Author : AX
# @File : __init__.py.py
# @Software: PyCharm

# 导入包
import requests
import re
from bs4 import BeautifulSoup


def request_data_url(url):
    headers = {
    'User-Agent': r'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KH'
    r'TML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }
    html = requests.get(url=url,headers=headers).text

    # 临时Debug
    # file = open("temp.html", encoding='utf-8')
    # html = file.read()
    # print(html)

    # 定义最后结果
    data = {}
    data['banners'] = []

    data['movies'] = []
    data['opera'] = []
    data['comic'] = []
    data['comprehensive'] = []

    # 解析html
    home_page_soup = BeautifulSoup(html, 'html.parser')

    # 首先解析banners属性轮播图
    banners = home_page_soup.select(".carousel a.stui-vodlist__thumb")
    # print(banners)
    for item in banners:
        # 取出title并去掉空格
        title = str(item.get('title')).strip()
        href = 'https://www.qiyeok.com' + str(item.get('href'))
        # print(title)
        # 取出图片
        img = str(item.get('style'))
        img_url = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]"
                             r"|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F"
                             r"][0-9a-fA-F]))+", img)
        img_url = img_url[0][:-1]
        # print(img_url)
        banner = {
            'title': title,
            'imgUrl': img_url,
            'href': href
        }
        data['banners'].append(banner)

    # 解析电影,由于其他的高度相似，直接一次写
    four_item = home_page_soup.select(".stui-vodlist")
    four_item_datas = []
    for item in four_item:
        # 分栏数据
        temp_item_datas = []
        current_soup = BeautifulSoup(str(item), 'html.parser')
        li_list = current_soup.select("li.col-md-5")
        # print(li_list)
        for current_li in li_list:
            temp_a = current_li.a
            # print(temp_a)
            # img_url
            img_url = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]"
                                 r"|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F"
                                 r"][0-9a-fA-F]))+", str(temp_a))[0]
            title = str(temp_a.get('title')).strip()
            href = 'https://www.qiyeok.com' + str(temp_a.get('href'))
            # 动态
            temp_span = temp_a.select('span')[1].string

            # 演员
            temp_p = current_li.select('p.text')[0].string
            # print(temp_p)
            # print(img_url, title, href, temp_span)
            temp = {
                'title': title,
                'imgUrl': img_url,
                'href': href,
                'desc': temp_span,
                'actors':temp_p
            }
            temp_item_datas.append(temp)
        four_item_datas.append(temp_item_datas)
    data['movies'] = four_item_datas[0]
    data['opera'] = four_item_datas[1]
    data['comic'] = four_item_datas[2]
    data['comprehensive'] = four_item_datas[3]

    # print(data)
    return data

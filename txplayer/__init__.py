# -*- coding:utf-8 -*-
# @Time : 2020/7/10 17:52
# @Author : AX
# @File : __init__.py.py
# @Software: PyCharm

import requests
import re
from bs4 import BeautifulSoup
import json


# 爬取腾讯视频 ＋ 调用解析
def home_page_data():
    # headers = {
    #     'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    #                   r' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    # }
    # html = requests.get(url="https://v.qq.com/", headers=headers)
    # html.encoding="utf-8"
    # html = html.text
    file = open("temp.html", "r", encoding="utf-8")
    html = file.read()

    # print(html)
    html = BeautifulSoup(html, 'html.parser')

    # 定义要返回的结果
    data = {
        "banners": [],
    }
    # 开始进行正则解析
    # 首先解析banners
    banners = html.select("a.slider_figure")
    print(len(banners))
    for banner in banners:
        # if banner.span:
        # print(banner)
        current = {}
        # 链接
        current["playerUrl"] = banner.get("href")
        # 标题
        temp_title = banner.select(".slider_figure_title")[0]
        current["title"] = temp_title.get("title")

        # 描述
        temp_des = banner.select(".slider_figure_desc2")[0]
        # print(temp_des)
        current["desc"] = temp_des.get("title")

        # 更新状态
        temp_status = banner.select(".slider_figure_desc")[0]
        if temp_status.get("data-update"):
            current["updateStatus"] = temp_status.get("data-update")
        else:
            current["updateStatus"] = ''
        # 图片链接
        # 由于存在懒加载
        # print(banner.img)
        temp_img = banner.img
        if temp_img.get("lz_next"):
            current["imgSrc"] = "https:" + temp_img.get("lz_next")
        elif temp_img.get("src"):
            current["imgSrc"] = "https:" + temp_img.get("src")
        # print(current)
        data["banners"].append(current)

    # 解析电影等元素
    total_element = html.select(".mod_row_box")
    # print(len(total_element))
    element = total_element[0]
    # print(element)
    # 确定名称
    name = element.get("id")
    if name and re.match(r"new_vs_hot_", name):
        current_name = name[11:]
        data[current_name] = []
    item_list = element.select(".list_item")
    for current_item in item_list:
        temp = {}
        # print(current_item)
        # 拿到href
        # print(current_item.a.get("href"))
        temp["href"] = current_item.a.get("playerUrl")
        if temp["href"]:
            # 拿到title
            temp_img = current_item.img
            temp["title"] = temp_img.get("alt")
            temp["imgSrc"] = "https:" + temp_img.get("src")
            data[current_name].append(temp)

    print(data)


def searchTXplayer(keyword):
    #  https://v.qq.com/x/search/?q=斗罗大陆&stag=0&smartbox_ab=
    headers = {
        'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) App'
                      r'leWebKit/537.36 (KHTML, like Gecko) Chrome/83'
                      r'.0.4103.116 Safari/537.36'
    }
    response = requests.get('https://v.qq.com/x/search/?q=' + str(keyword) + '&stag=0&smartbox_ab=')
    # print(response.text)
    html = BeautifulSoup(str(response.text), 'html.parser')
    # 返回带有剧集的结果：
    result_items = html.select(".result_item_v")
    # print(result_items)
    result = []
    print(len(result_items))
    for item in result_items:
        temp = {
            "id": "",
            "imgSrc": "",
            "title": "",
            "desc": "",
            "current_status": "",
            "current_count": 1
        }
        img = item.select(".figure_pic")
        # 图片
        temp["imgSrc"] = "https:" + img[0].get("src")
        # 状态
        temp["current_status"] = item.select(".figure_info")[0].string or "无集数信息"
        # 集数
        temp["current_count"] = (re.search(r"\d+", temp["current_status"]) and (
            int(re.search(r"\d+", temp["current_status"]).group()))) or 0

        # id
        temp_a = item.select(".result_title")[0].a
        temp["id"] = temp_a.get("href")[len("https://v.qq.com/detail/m/"):-5]

        # 简介
        temp["desc"] = list(item.select(".desc_text")[0].children)[0].strip()
        # 标题
        for temp_str in list(temp_a.children):
            temp["title"] = temp["title"] + temp_str.string.strip()

        # 最新集数

        # print(temp)
        result.append(temp)
    return result


def get_page_message(id, count):
    response = requests.get(r"https://s.video.qq.com/get_playsource?" \
                            r"id=" + id + "&plat=2&type=4&" \
                                          r"data_type=2&video_type=3&range=1-" + count + "&" \
                                                                                         r"plname=qq&otype=json&num_mod_cnt=20&" \
                                                                                         r"callback=_jsonp_2_9081&_t=1595256007313")
    ans = json.loads(response.text[14:-1])
    print(ans)
    print(type(ans))
    return ans

# 拿到最后一集
# test_find = html.select(".result_episode_list")[0]
# count = test_find.select(".item")[-2]
# id = count.select("a")[0].get("href")[len("https://v.qq.com/x/cover/"):]
# id = id[:str(id).find("/")]
# print(id)
# count = count.select("a")[0].string
# print(count)
# 调用接口读取数据
# ans = get_page_message(id, count)
# return ans

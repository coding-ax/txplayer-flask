# -*- coding:utf-8 -*-
# @Time : 2020/7/10 17:10
# @Author : AX
# @File : __init__.py.py
# @Software: PyCharm

import requests


# 随机返回网易云一首歌或者返回mid指定的歌

# 接口地址：https://api.uomg.com/api/rand.music
# 返回格式：json/mp3
# 请求方式：get/post
# 请求示例：https://api.uomg.com/api/rand.music?sort=热歌榜&format=json
#
# 请求参数说明：
# 	名称 	必填 	类型 	说明
#   	sort 	否 	string 	选择输出分类[热歌榜|新歌榜|飙升榜|抖音榜|电音榜]，为空输出热歌榜
#   	mid 	否 	int 	网易云歌单ID
#   	format 	否 	string 	选择输出格式[json|mp3]
# 返回参数说明：
# 	名称 	类型 	说明
#   	code 	string 	返回的状态码
#   	data 	string 	返回歌曲数据
#   	msg 	string 	返回错误提示信息！


def random_music(sort="热歌榜", mid=None, format="json"):
    response = requests.get("https://api.uomg.com/api/rand.music?sort=" + sort + "&format=" + format)
    # print(response.json())
    return response.json()


# 查询音乐
# 基本说明：
# 接口地址：https://api.apiopen.top/searchMusic
# 返回格式：json
# 请求方式：get/post
# 请求示例：https://api.apiopen.top/searchMusic?name=我爱你
# 请求参数说明：
# 名称	类型	必填	说明
# name	String	必填	音乐名称
# 返回参数说明：
# 名称	类型	说明
# code	int	状态码
# message	string	提示消息
# result	array	结果集合
def music_get(name):
    response = requests.get("https://api.apiopen.top/searchMusic?name=" + name)
    return response.json()

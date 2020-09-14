# -*- coding:utf-8 -*-
# @Time : 2020/7/10 17:53
# @Author : AX
# @File : test.py
# @Software: PyCharm

import txplayer

if __name__ == '__main__':
    data = txplayer.searchTXplayer('武庚纪')
    data = txplayer.get_page_message(data[0]['id'], str(data[0]['current_count']))
    print(data)

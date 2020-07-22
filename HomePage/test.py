# -*- coding:utf-8 -*-
# @Time : 2020/7/9 20:39
# @Author : AX
# @File : test.py
# @Software: PyCharm

import HomePage

if __name__ == '__main__':
    data = HomePage.request_data_url("http://www.qiyeok.com/")
    print(data)
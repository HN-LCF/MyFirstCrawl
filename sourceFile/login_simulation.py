# -*- coding: utf-8 -*-
"""
@File       :login_simulation.py
@Time       :2021/2/24 21:06
@Author     :HN-LCF
@Email      :lou116211@outlook.com
@Software   :PyCharm
"""

# todo:
#   - cookie
#   - 代理机制
#   - 验证码识别
#   - 模拟登录

import requests
import json

from lxml import etree


def information_crawl():
    """
    爬取雪球网的资讯信息--'https://xueqiu.com/'

    破解cookie反爬：
        通过Session对象解决需要携带cookie的页面请求
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 FS '
    }

    session = requests.Session()  # 创建Session对象用以在首次请求中捕获并存储cookie
    main_url = 'https://xueqiu.com/'
    session.get(main_url, headers=headers)  # 捕获且存储cookie

    url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=173348&size=15'
    page_text = session.get(url=url, headers=headers).json()  # Session携带cookie发起的请求
    print(page_text)

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
import random
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


def crawl_with_proxy():
    """
    通过代理服务器发起请求访问页面数据
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 FS '
    }

    ## 封装代理池
    proxy_url = 'API_url'
    proxy_page_text = url_requests(proxy_url)
    proxy_tree = url_parse(proxy_page_text)
    proxy_list = proxy_tree.xpath('//body//text()')
    http_proxy = []  # 代理池
    for proxy in proxy_list:
        dic = {
            'https': proxy
        }
        http_proxy.append(dic)

    ## 使用代理发起请求
    target_url = 'https://www.xicidaili.com/nn/%d'  # 爬取西祠代理网站免费代理ip与端口被
    ips = []
    for page in range(1, 11):
        target_url = format(target_url % page)
        target_page_text = url_requests(target_url, proxies=random.choice(http_proxy))  # 随机选择代理池内ip与相应端号发起请求
        target_tree = url_parse(target_page_text)
        tr_list = target_tree.xpath('//*[@id="ip_list"]//tr')[1:]
        for tr in tr_list:
            ip = tr.xpath('./td[2]/text()')[0]
            ips.append(ip)
    print(len(ips))  # 测试代理服务器效果


def identify_verification_code():
    """
    验证码识别
    """




def url_requests(url, **kwargs):
    """
    访问url请求页面源码

    :params
        url--目标页面地址
    :return
        page_text--由requests访问url请求到的text格式的页面源码数据
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 FS '
    }

    page = requests.get(url=url, headers=headers, **kwargs)
    page.encoding = 'utf-8'
    page_text = page.text
    return page_text


def url_session(cookie_url, target_url, **kwargs):
    """
    通过requests的Session对象访问url请求页面源码

    :params
        main_url--捕获cookie的页面url
        target_url--所要获取源码数据所在页面的url
    :return
        page_text--由Session访问url请求到的text格式的页面源码数据
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 FS '
    }

    session = requests.Session()  # 创建Session对象用以在首次请求中捕获并存储cookie
    session.get(cookie_url, headers=headers)  # 捕获且存储cookie
    page_text = session.get(url=target_url, headers=headers, **kwargs).json()  # Session携带cookie发起的请求
    return page_text


def url_parse(page_text):
    """
    页面文本数据解析

    :params
        page_text--由requests访问url请求到的text格式的页面源码数据
    :return
        tree--经etree类实例解析后的页面源码
    """

    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(page_text, parser=parser)
    return tree

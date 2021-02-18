# -*- coding: utf-8 -*-
"""
@File       :novelCrawl_biqu6.py
@Time       :2021/2/18 20:00
@Author     :HN-LCF
@Email      :lou116211@outlook.com
@Software   :PyCharm
"""

# todo:
#   -一个通用的笔趣阁小说的爬虫模板

import os
import re

import requests
from lxml import etree

biqu_url = 'http://www.biqu6.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
}


def contentRequests(novel_url, n_min, n_num):
    con_novel_list = []
    con_page = requests.get(url=novel_url, headers=headers)
    con_page.encoding = 'utf-8'
    con_page_text = con_page.text

    parser = etree.HTMLParser(encoding="utf-8")
    con_tree = etree.HTML(con_page_text, parser=parser)
    n_min = n_min
    n_max = n_num
    for i in range(n_min, n_max):
        con_title = con_tree.xpath('//div[@id="list"]//dd[' + str(i) + ']/a/text()')[0]
        con_url = biqu_url + con_tree.xpath('//div[@id="list"]//dd[' + str(i) + ']/a/@href')[0]
        con_novel_dic = {
            'title': con_title,
            'url': con_url
        }
        con_novel_list.append(con_novel_dic)
    return con_novel_list


def detailRequests(con_novel_list, novelName):
    novel_list = con_novel_list
    novelName = novelName
    fileName = 'BiQuGe'
    if not os.path.exists(fileName):
        os.makedirs(fileName)
    for novel in novel_list:
        chap_title = novel.get('title')
        chap_url = novel.get('url')
        chap_page = requests.get(url=chap_url, headers=headers)
        chap_page.encoding = 'utf-8'
        chap_page_text = chap_page.text
        parser = etree.HTMLParser(encoding="utf-8")
        chap_tree = etree.HTML(chap_page_text, parser=parser)
        chap_detail = chap_tree.xpath('//div[@id="content"]/text()')
        novel_detail = ''
        for detail in chap_detail:
            novel_detail = novel_detail + detail.replace('\xa0\xa0\xa0\xa0', '\r\t')
        # 爬取单章节小说
        # fp = open('./' + fileName + '/' + chap_title + '.txt', 'w', encoding='utf-8')
        novel_detail = re.sub('\s+', '\r\n\t', novel_detail).strip('\r')
        # fp.write(chap_title + '\n' + novel_detail + '\n')
        # fp.close()
        with open('./BiQuGe/' + novelName + '.txt', 'a+', encoding='utf-8') as fp:
            fp.write(chap_title + '\n' + novel_detail + '\n')
        print(chap_title, '爬取成功！！！')
    print('\r\r\r', novelName, '爬取完成！！！')
    fp.close()


def demo():
    novelName = str(input('请输入小说名：'))
    n_min = int(input('请输入正文之上有几章：'))
    n_num = int(input('请输入小说章节总数：')) + 55
    novelUrl = str(input('请输入小说Url：'))
    detailRequests(contentRequests(novelUrl, n_min, n_num), novelName)

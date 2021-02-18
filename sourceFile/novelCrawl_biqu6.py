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

file_name = 'BiQuGe'
if not os.path.exists(file_name):
    os.makedirs(file_name)

biqu_url = 'http://www.biqu6.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
}


def Request(url):
    page = requests.get(url=url, headers=headers)
    page.encoding = 'utf-8'
    page_text = page.text
    return page_text


def Parse(page_text):
    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(page_text, parser=parser)
    return tree


def ChapLocate(chap_tree, chap_start, chap_end):
    chap_list = []
    for i in range(chap_start, chap_end):
        chap_title = chap_tree.xpath('//div[@id="list"]//dd[' + str(i) + ']/a/text()')[0]
        chap_url = biqu_url + chap_tree.xpath('//div[@id="list"]//dd[' + str(i) + ']/a/@href')[0]
        chap_dic = {
            'title': chap_title,
            'url': chap_url
        }
        # print(chap_title)
        chap_list.append(chap_dic)
    return chap_list


def ConLocate(con_tree):  # 章节内容定位提取
    """
    返回单章的标题与内容
    :param con_tree
    :return:
    """
    con_detail = []
    con_detail = con_tree.xpath('//div[@id="content"]/text()')
    return con_detail


def TextFormat(con_detail):
    chap_detail = ''
    for detail in con_detail:
        chap_detail = chap_detail + detail.replace('\xa0\xa0\xa0\xa0', '\r\t')
    chap_detail = re.sub('\s+', '\r\n\t', chap_detail).strip('\r')
    return chap_detail


def WriteFile(novel_name, chapter):
    novel_name = novel_name
    # 爬取单章节小说
    # fp = open('./' + file_name + '/' + chap_title + '.txt', 'w', encoding='utf-8')
    # fp.write(chap_title + '\n' + chap_detail + '\n')
    # fp.close()
    with open('./' + file_name + '/' + novel_name + '.txt', 'a+', encoding='utf-8') as fp:
        fp.write(chapter.get('title') + '\n' + chapter.get('content') + '\n')
    fp.close()
    print(chapter.get('title'), '爬取成功！！！')


def demo():
    novel_name = str(input('请输入小说名：'))
    chap_start = int(input('请输入正文之上有几章：'))
    chap_end = int(input('请输入小说章节总数：')) + 126
    novel_url = str(input('请输入小说Url：'))
    chap_page_text = Request(novel_url)
    chap_tree = Parse(chap_page_text)
    chap_list = ChapLocate(chap_tree, chap_start, chap_end)

    for chap in chap_list:
        chap_title = chap.get('title')
        chap_url = chap.get('url')
        con_page_text = Request(chap_url)
        con_tree = Parse(con_page_text)
        con_detail = ConLocate(con_tree)
        chap_detail = TextFormat(con_detail)
        chapter = {}
        chapter.update({'title': chap_title, 'content': chap_detail})
        WriteFile(novel_name, chapter)
    print('\r\r\r', novel_name, '爬取完成！！！')

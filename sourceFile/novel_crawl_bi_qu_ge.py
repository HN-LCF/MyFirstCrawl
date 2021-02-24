# -*- coding: utf-8 -*-
"""
@File       :novel_crawl_bi_qu_ge.py
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

file_name = 'bi_qu_ge'
bi_qu_url = 'http://www.biqu6.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
}


class BiQuGe(object):
    def __init__(self, novel_dict):
        self.file_name = file_name
        self.bi_qu_url = bi_qu_url
        self.headers = headers
        self.novel_name = novel_dict["novel_name"]
        self.novel_url = novel_dict["novel_url"]
        self.chapter_start = novel_dict["chapter_start"]
        self.chapter_end = novel_dict["chapter_end"]

    def is_novel_file(self):
        """
        确认小说存储目录是否存在
        不存在，则创建该文件夹
        """

        if not os.path.exists(self.file_name):
            os.makedirs(self.file_name)

    def url_requests(self, url):
        """
        访问url请求页面源码

        :params
            url--目标页面地址
        :return
            page_text--由requests访问url请求到的text格式的页面源码数据
        """

        page = requests.get(url=url, headers=self.headers)
        page.encoding = 'utf-8'
        page_text = page.text
        return page_text

    def url_parse(self, page_text):
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

    def chapter_locate(self, chap_tree):
        """
        章节名称与相应url的定位与提取

        :params
            chap_tree--解析后的目录页内容
            chap_start--爬取的起始目录条目数
            chap_end--小说总章节目录数
        :return
            chap_list--章节url字典
            {
                'title': chap_title,
                'url': chap_url
            }
        """

        chap_list = []
        for i in range(self.chapter_start, self.chapter_end):
            chap_title = chap_tree.xpath('//div[@id="list"]//dd[' + str(i) + ']/a/text()')[0]
            chap_url = bi_qu_url + chap_tree.xpath('//div[@id="list"]//dd[' + str(i) + ']/a/@href')[0]
            chap_dic = {
                'title': chap_title,
                'url': chap_url
            }
            # print(chap_title, chap_url)
            chap_list.append(chap_dic)
        return chap_list

    def content_locate(self, con_tree):
        """
        章节内容定位提取

        :params
            con_tree--解析后章节内容源码
        :return
            con_detail--定位后提取的章节内容（未格式化）
        """

        con_detail = con_tree.xpath('//div[@id="content"]/text()')
        return con_detail

    def content_format(self, con_detail):
        """
        将爬取的小说章节内容格式化

        1.替换掉特殊字符并排版
        2.返回格式化的小说单章节内容
        :params
            con_detail--定位后提取的章节内容（未格式化）
        :return
            chap_detail--排版后的章节内容
        """

        chap_detail = ''
        for detail in con_detail:
            chap_detail = chap_detail + detail.replace('\xa0\xa0\xa0\xa0', '\r\t')
        chap_detail = re.sub('\s+', '\r\n\t', chap_detail).strip('\r')
        # print(chap_detail)
        return chap_detail

    def write_to_file(self, chapter):
        """
        将小说章节名与相应章节内容写入txt文件

        1.打开文件
        2.写入内容
        3.关闭文件
        4.提示写入章节爬取成功
        :params
            novel_name--爬取小说名称
            chapter--章节字典
            {
                "title":章节名称,
                "content":章节内容
            }
        :return
            提示爬取成功
        """

        novel_name = self.novel_name
        # 爬取单章节小说
        # fp = open('./' + file_name + '/' + chap_title + '.txt', 'w', encoding='utf-8')
        # fp.write(chap_title + '\n' + chap_detail + '\n')
        # fp.close()
        with open('../' + file_name + '/' + novel_name + '.txt', 'a+', encoding='utf-8') as fp:
            fp.write(chapter.get('title') + '\n' + chapter.get('content') + '\n')
        fp.close()
        print(chapter.get('title'), '爬取成功！！！')


if __name__ == '__main__':

    novel_name = str(input('请输入小说名：'))
    novel_url = str(input('请输入小说Url：'))
    chap_start = int(input('请输入正文之上有几章：'))
    chap_end = int(input('请输入小说章节总数：')) + 126

    novel_dict = {
        'novel_name': novel_name,
        'novel_url': novel_url,
        'chapter_start': chap_start,
        'chapter_end': chap_end
    }
    bi_qu_novel = BiQuGe(novel_dict)
    chap_page_text = bi_qu_novel.url_requests(novel_url)
    chap_tree = bi_qu_novel.url_parse(chap_page_text)
    chap_list = bi_qu_novel.chapter_locate(chap_tree)

    for chap in chap_list:
        chap_title = chap.get('title')
        chap_url = chap.get('url')
        con_page_text = bi_qu_novel.url_requests(chap_url)
        con_tree = bi_qu_novel.url_parse(con_page_text)
        con_detail = bi_qu_novel.content_locate(con_tree)
        chap_detail = bi_qu_novel.content_format(con_detail)
        chapter = {}
        chapter.update({'title': chap_title, 'content': chap_detail})
        bi_qu_novel.write_to_file(chapter)
    print('\r\r\r', novel_name, '爬取完成！！！')

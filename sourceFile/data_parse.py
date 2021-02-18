"""
数据分析：
正则，bs4，xpath，pyquery

"""
import os
import re
import urllib.request

import requests
from bs4 import BeautifulSoup
from lxml import etree


def imageCrawl_requests():
    """
    requests直接抓取图片
    with持续化存储
    :return: 一个jpg文件
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
    }
    img_url = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fa2.att.hudong.com%2F74%2F24' \
              '%2F23300001248577135219240898162.jpg&refer=http%3A%2F%2Fa2.att.hudong.com&app=2002&size=f9999,' \
              '10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1616133427&t=8cc5c8563e57dabed1cf2eeebe33e886 '
    response = requests.get(url=img_url, headers=headers)
    # content返回的是二进制形式的响应数据
    img_data = response.content
    with open('./1.jpg', 'wb') as fp:
        fp.write(img_data)


def imageCrawl_urllib():
    """
    利用urllib中request类的urlretrieve方法
    直接从图片url进行爬取并保存
    :return: 一个jpg文件
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
    }
    img_url = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fa2.att.hudong.com%2F74%2F24' \
              '%2F23300001248577135219240898162.jpg&refer=http%3A%2F%2Fa2.att.hudong.com&app=2002&size=f9999,' \
              '10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1616133427&t=8cc5c8563e57dabed1cf2eeebe33e886 '
    # urlretrieve方法可以直接对url发起请求并进行持久化存储
    urllib.request.urlretrieve(img_url, './2.jpg')


def batchImageCrawl():
    """
    从校花网中批量爬取图片（无动态加载数据）
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
    }
    # 1.捕获当前页面源码数据
    url = 'https://nice.ruyile.com/'
    page_text = requests.get(url=url, headers=headers).text

    # 2.从当前获取的页面源码数据中解析出图片url
    ex = '<div class="tp_a">.*?<img src="(.*?)" alt=.*?</div>'
    img_src_list = re.findall(ex, page_text, re.S)

    # 3.新建一个文件夹存储图片
    dirName = 'ImgLibs'
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    # 4.根据图片地址src进行爬取并存储到预新建文件夹
    for src in img_src_list:
        imgPath = dirName + '/' + src.split('/')[-1]
        urllib.request.urlretrieve(src, imgPath)
        print(imgPath, '下载成功！！！')


"""
../ 表示当前文件所在的目录的上一级目录
./ 表示当前文件所在的目录(可以省略)
/ 表示当前站点的根目录(域名映射的硬盘目录)
"""


def pageParse_bs4():
    """
    使用bs4的BeautifulSoup类解析网页Html代码
    操作：
        1.实例化对象
        2.定位所需标签
        3.取文本、取属性
    :return:
    """
    fp = open('./Test/test_parse.html', 'r', encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(fp, 'lxml')
    # soup.p
    # soup.find('li', class_='level2')
    # soup.findAll('li', class_='level2')
    # soup.select('.level2')
    pTag = soup.findAll('p')
    for tag in pTag:
        print(tag.string)
    liTag = soup.select('.tag > ul > li > span > a')
    for tag in liTag:
        print(tag['href'])
    # tag['attrName']--标签属性
    # tag.text/string--标签文本


def novelCrawl():
    """
    爬取《三国演义》小说全篇
    url：https://www.shicimingju.com/book/sanguoyanyi.html
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
    }
    main_url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    fp = open('./TextLibs/sanguo.txt', 'w', encoding='utf-8')
    page = requests.get(url=main_url, headers=headers)
    page.encoding = 'utf-8'
    page_text = page.text
    # 数据解析：章节标题，详情页url，章节内容
    m_soup = BeautifulSoup(page_text, 'lxml')
    # 所有目录所在的a标签（列表）
    a_list = m_soup.select('.book-mulu > ul > li > a')
    for a in a_list:
        title = a.string
        detail_url = 'https://www.shicimingju.com/' + a['href']
        # 对详情页发起请求解析内容
        page_detail = requests.get(url=detail_url, headers=headers)
        page_detail.encoding = 'utf-8'
        page_text_detail = page_detail.text
        d_soup = BeautifulSoup(page_text_detail, 'lxml')
        chapter_tag = d_soup.find('div', class_='chapter_content')
        chapter = chapter_tag.text
        fp.write(title + ':' + chapter + '\n')
        print(title, '保存成功!!!')
    fp.close()


def pageParse_xpath():
    """

    -----------------------------------------------------------------
    * 标签定位：
        * 路径定位--meta:
            tree.xpath('/html/head/meta')
            tree.xpath('/html//meta')
            tree.xpath('//meta')
        * 属性定位：
            tree.xpath('//div[@class="tag"]//li')
        * 引定位：
            tree.xpath('//div[@class="tag"]//li[1]')
    * 取文本：
        tree.xpath('//a[@id="fang"]/text()')
    * 取属性：
        tree.xpath('//a[@id="fang"]/@href')
    :return:
    """
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.parse('./Test/test_parse.html', parser=parser)
    a = tree.xpath('//a[@id="fang"]/@href')
    print(a)
    print(isinstance(a, list))

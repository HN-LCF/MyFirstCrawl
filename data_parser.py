"""
数据分析：
正则，bs4，xpath，pyquery

"""
import os
import re
import urllib.request

import requests


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

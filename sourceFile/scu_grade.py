# -*- coding: utf-8 -*-
"""
@File       :scu_grade.py
@Time       :2021/3/5 17:37
@Author     :HN-LCF
@Email      :lou116211@outlook.com
@Software   :PyCharm
"""

# todo:
#   -通过教务处本科登录系统爬取考生成绩
#   -模拟登录
#   -爬取成绩页面url
#   -爬取成绩信息
#   -整理成绩信息

import requests
import json
from lxml import etree
from PIL import Image


def demo():
    """

    """

    main_url = 'http://zhjw.scu.edu.cn/'
    login_url = 'http://zhjw.scu.edu.cn/login'  # 登陆页面url
    session = requests.Session()  # 创建Session对象用以在首次请求中捕获并存储cookie
    latter_cookie = session.get(login_url).headers['Set-Cookie'][11:-8]  # 捕获且存储cookie
    headers = {
        'Cookie': 'JSESSIONID=' + latter_cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 FS ',
        'Referer': 'http://zhjw.scu.edu.cn/login'
    }

    ## 爬取验证码图片
    login_page_text = session.get(url=login_url, headers=headers).text
    parser = etree.HTMLParser(encoding='utf-8')
    login_page_tree = etree.HTML(login_page_text, parser=parser)
    img_url = main_url + login_page_tree.xpath('//*[@id="captchaImg"]/@src')[0]
    img_data = session.get(url=img_url, headers=headers).content  # 获取验证码图片数据
    with open('./code.jpg', 'wb') as fp:  # 保存验证码到本地
        fp.write(img_data)
    img = Image.open('./code.jpg')  # 打开验证码图片
    img.show()

    ## 模拟登录，爬取页面数据
    rand_code = input('请输入验证码：')
    after_login_url = 'http://zhjw.scu.edu.cn/j_spring_security_check'
    data = {
        'j_username': '2019141410125',
        'j_password': 'd5d2cd913f974c1576b4d9f4481218f6',
        'j_captcha': rand_code,
    }
    after_login_page_text = session.post(url=after_login_url, headers=headers, data=data).text  # 获取了登陆成功后对应页面的源码数据
    after_login_page_tree = etree.HTML(after_login_page_text, parser=parser)
    grade_url = main_url + after_login_page_tree.xpath('//*[@id="125803405"]/a/@href')[0][:-5]+'data'
    grade_page_text = session.get(url=grade_url, headers=headers).text
    course_grade_list = json.loads(grade_page_text, strict=False)['list']['records']

    # grade_page_tree = etree.HTML(grade_page_text, parser=parser)
    # grade_item_list = grade_page_tree.xpath('//*[@id="scoreintbody"]/tr[1]/text()')
    for items in course_grade_list:
        with open('./gushiwen.txt', 'a', encoding='utf-8') as fp:
            fp.write(items[11])
            fp.write('\t')
            fp.write(items[12])
            fp.write('\n')


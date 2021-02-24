import json
import socket
import time

import requests


def general_crawl():
    """
    爬取搜狗首页面数据
    """
    # 指定url--搜狗首页
    url = 'https://www.sogou.com/'
    # 发起请求,get方法的返回值为响应对象
    response = requests.get(url=url)
    # 获取响应数据,以字符串形式返回
    pageText = response.text
    # 持久化存储
    with open('./sogou.html', 'w', encoding='utf-8') as fp:
        fp.write(pageText)


def web_collector(keyWord):
    """
    基于搜狗针对指定不同的关键字将其对应的页面数据进行爬取
    携带了请求参数url，并将url携带的参数进行动态化
    """
    # 伪装User-Agent作为请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    # 实现参数动态化
    params = {
        'query': keyWord
    }
    url = 'https://www.sogou.com/web'
    # params参数（字典）：保存请求时url携带的参数
    response = requests.get(url=url, params=params, headers=headers)
    response.encoding = 'utf-8'
    pageText = response.text
    fileName = keyWord + '.html'
    with open(fileName, 'w', encoding='utf-8') as fp:
        fp.write(pageText)
    print(fileName, '爬取成功')


def favorite_movie():
    """
    通过豆瓣爬取某类排行榜电影的详细信息
    电影名称name、评分score等
    用抓包工具获取所需动态数据数据包相关信息即可
    """
    # 伪装User-Agent作为请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    # 定位出动态数据对应数据包的url
    url = 'https://movie.douban.com/j/chart/top_list'
    # 字符串参数序列化为字典
    params = {
        'type': '5',
        'interval_id': '100:90',
        'action': '',
        'start': '0',
        'limit': '50',
    }
    response = requests.get(url=url, params=params, headers=headers)
    # .json()将获取的字符串形式的json数据序列化为字典或者列表对象
    pageText = response.json()
    # 解析出电影的名称与评分
    for movie in pageText:
        name = movie['title']
        score = movie['score']
        str = name + '\t' + score + '\n'
        with open('./douban.txt', 'a', encoding='utf-8') as fp:
            fp.write(str)


def page_crawl():
    """
    分页数据的爬取--以爬取肯德基餐厅位置的数据为例
    通过for循环对每一次Ajax请求的数据进行爬取并写入
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    for page in range(1, 9):
        data = {
            'cname': '',
            'pid': '',
            'keyword': '北京',
            'pageIndex': str(page),
            'pageSize': '80',
        }
        # data是post方法中处理参数动态化的参数
        response = requests.post(url=url, headers=headers, data=data)
        pageText = response.json()
        # 每一页餐厅个数归零
        i = 0

        ## 获取餐厅位置信息， 写入数据
        for dic in pageText['Table1']:
            title = dic['storeName'] + '餐厅'
            addr = dic['addressDetail']
            # 记录每页餐厅数目
            i = i + 1
            # 统计餐厅总数
            num = str((page - 1) * 10 + i)
            r_str = num + '、 ' + title + '\t' + addr + '\n'
            # 创建TXT文件并写入数据
            with open('./restaurant.txt', 'a', encoding='utf-8') as fp:
                fp.write(r_str)


def cosmetics_crawl():
    """
     任务：爬取药监总局中的企业详情数据
     url：<http://scxk.nmpa.gov.cn:81/xk/>
     需求：
         将首页中每一家企业的详情数据进行爬取
     步骤：
         1. 先对化妆品企业的目录页数据进行爬取，获得企业相应详情页对应的post参数--id
         2. 根据企业id，爬取有关详细信息并存入文件

     Varibles:
         headers--伪装请求头
         pre_url--企业目录页地址
         pre_data--企业目录页post参数
         pre_response--企业目录页响应
         pre_pageText--企业目录页Json数据
         c_id--企业对应的详情页post参数
         pre_inf--目录页爬取的企业信息（企业名称，企业ID）
         ----------------------
         url--企业详情页地址
         data--企业详情页post参数
         response--企业详情页响应
         pageText--企业详情页Json数据，
         inf（information)--爬取的企业详细信息(字典）
    """

    socket.setdefaulttimeout(20)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    ##获取目录页所有企业的名称与id参数
    pre_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    for page in range(1, 8):
        pre_data = {
            'on': 'true',
            'page': str(page),
            'pageSize': '15',
            'productName': '',
            'conditionType': '1',
            'applyname': '',
            'applysn': '',
        }
        pre_response = requests.post(url=pre_url, headers=headers, data=pre_data)
        pre_response.close()
        pre_pageText = pre_response.json()
        for company in pre_pageText['list']:
            c_name = company['EPS_NAME']
            c_id = company['ID']
            pre_inf = {
                '企业名称': c_name,
                '许可证编号': c_id,
            }
            with open('./pre_company.txt', 'a', encoding='utf-8') as f:
                # 将字典以Json数据格式写入文件，设置缩进量indent为4
                json.dump(pre_inf, f, ensure_ascii=False, indent=4)
            # 根据爬取的企业id参数，爬取详情页的企业信息
            url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
            data = {
                'id': c_id
            }
            response = requests.post(url=url, headers=headers, data=data)
            response.close()
            pageText = response.json()
            inf = {
                '企业名称': pageText['epsName'],
                '许可证编号': pageText['productSn'],
                '许可项目': pageText['certStr'],
                '企业住所': pageText['epsAddress'],
                '生产地址': pageText['epsProductAddress'],
                '社会信用代码': pageText['businessLicenseNumber'],
                '法定代表人': pageText['legalPerson'],
                '企业负责人': pageText['businessPerson'],
                '质量负责人': pageText['qualityPerson'],
                '发证机关': pageText['qfManagerName'],
                '签发人': pageText['xkName'],
                '日常监督管理机构': pageText['rcManagerDepartName'],
                '日常监督管理人员': pageText['rcManagerUser'],
                '有效期至': pageText['xkDate'],
                '发证日期': pageText['xkDateStr'],
                '状态': pageText['isimport'],
                '投诉举报电话': str(1233)
            }
            with open('./company.txt', 'a', encoding='utf-8') as fp:
                # 将字典以Json数据格式写入文件，设置缩进量indent为4
                json.dump(inf, fp, ensure_ascii=False, indent=4)

            time.sleep(1)

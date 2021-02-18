
# 一、Python爬虫

## 1 基础知识

### 1.1 项目概要

* 项目名称：Python爬虫
* [B站视频地址：https://www.bilibili.com/video/BV135411H7yR](https://www.bilibili.com/video/BV135411H7yR)
* 课程时长：四周
* 讲解内容：
  * 爬虫：七天
    * requests模块
      * 数据解析
      * 动态加载数据的爬取
      * selenium
      * 移动端数据的爬取
      * 异步的爬虫
      * 10种反爬机制
    * scrapy框架
      * 异步的爬虫框架
  * 数据分析：四天
    * numpy、pandas、matplotlib模块
    * 基于相关的实战案例巩固技能
      * 人口分析
      * 政治献金数据分析
      * 用户消费行为分析
    * 金融量化
      * 股票策略的实现
        * 双均线的策略
  * 算法与数据结构：三天
    * 目的：应付面试
    * 数据结构：
      * 栈、队列、链表、二叉树
    * 算法：
      * 选择、冒泡、插入、希尔排序、快速排序
      * 二分查找
    * 面试题
  * 机器学习：八天
    * 机器学习的基本概述
    * 机器学习中的基本概念
    * 特征工程
    * 几个算法模型

---

### 1.2 爬虫概述

* 什么是爬虫
  * 爬虫是通过编写程序，让其**模拟**浏览器上网，然后再互联网中**抓取**数据的过程。
  * 关键词抽取
    * 模拟：浏览器是纯天然最原始的爬虫工具。
    * 抓取：
      * 抓取一整张的页面源码数据
      * 抓取一整张页面的局部数据
* 爬虫的分类：
  * 通用爬虫：
    * 爬取一整张页面源码数据包
  * 聚焦爬虫：
    * 爬取一整张页面的局部数据
    * 补充：建立在通用爬虫的基础之上
  * 增量式爬虫：
    * 用来**监测**网站数据更新的情况，以便爬取到网站最新更新过的数据
  * 分布式爬虫：
    * 提高爬取效率的终极武器（**高并发、分布式**）
* 反爬机制：
  * 作用于门户网站中。如果网站不想让爬虫轻易爬取到数据，它可以制定相关的机制或措施阻止爬虫爬取其数据
* 反反爬策略：
  * 作用于爬虫程序中。爬虫可以制定相关的策略破击反爬机制从而爬取到相关的数据

* **第一种反爬机制**
  * 1. robots协议--防君子不防小人
    * 是一个纯文本的协议，协议中规定了该网站中哪些数据可以被哪些爬虫爬取，哪些不可以被爬取
    * 该协议可主观不遵从

---

## 2 技术模块

### 2.1 requests模块

* requests
  * 爬虫中一个基于网络请求的模块
  * 安装：pip install requests
  * 作用：模拟浏览器发起请求
  * 编码流程：
    * 1.指定url
    * 2.发起请求
    * 3.获取响应数据（即爬取到的页面源码数据）
    * 4.持久化存储

### 2.2 requests应用案例

> **1. 爬取搜狗页面原始数据**

```python
import requests

def generalCrawl():
    '''
    爬取搜狗首页面数据
    '''
    #指定url--搜狗首页
    url = 'https://www.sogou.com/'
    #发起请求,get方法的返回值为响应对象
    response = requests.get(url = url)
    #获取响应数据,以字符串形式返回
    pageText = response.text
    #持久化存储
    with open('./sogou.html', 'w', encoding = 'utf-8') as fp:
            fp.write(pageText)
```

> **2. 设计一个简易网页采集器**
>
> 基于搜狗针对指定不同的关键字将其对应的页面数据进行爬取
> 参数动态化：
> > 如果请求的url携带参数，且我们想要将携带的参数进行动态化操作，则：
> >
> > 1. 将携带的动态参数封装为字典
> > 2. 将该字典作用到requests的get方法的params参数中即可
> > 3. 将原始url中的参数删除

```python
import requests

def webCollector(keyWord):
    '''
    基于搜狗针对指定不同的关键字将其对应的页面数据进行爬取
    携带了请求参数url，并将url携带的参数进行动态化
    '''
    #实现参数动态化
    params = {
        'query':keyWord
        }
    url = 'https://www.sogou.com/web?'
    #params参数（字典）：保存请求时url携带的参数
    response = requests.get(url = url, params = params)
    response.encoding = 'utf-8'
    pageText = response.text
    fileName = keyWord + '.html'
    with open(fileName, 'w', encoding = 'utf-8') as fp:
            fp.write(pageText)
    print(fileName, '爬取成功')
```

* 运行结果：采集器收集页面显示【**异常的访问**】请求导致请求数据的缺失
  * 异常的访问请求：
    * 网站后台已经检测出此次请求并**不是由浏览器发起的**而是通过爬虫发起的请求
  * 网站的后台如何检测请求是否由浏览器发起的？
    * 通过判定请求的请求头中**User-Agent**
  * 什么是User-Agent？
    * 即**请求载体**的身份标识
    * 请求载体
      * 浏览器
        * 浏览器的身份标识固定，可以从抓包工具中获取
      * 爬虫程序
        * 身份标识各自不同

* **第二种反爬机制**
  * UA检测：网站后台会检测请求对应的User-Agent，以判定当前请求是否异常
* 反反爬策略
  * **UA伪装：被作用于绝大多数网站中，日后的爬虫程序均默认进行UA伪装**
  * 伪装流程：
    * 从抓包工具中捕获到一个基于浏览器请求的User-Agent的值，并将其伪装作用到一个字典中，将该字典作用到请求方法（get， post）的headers参数中即可

> **３. 实现了UA伪装的简易网页采集器**

```python
import requests

def webCollector(keyWord):
    '''
    基于搜狗针对指定不同的关键字将其对应的页面数据进行爬取
    携带了请求参数url，并将url携带的参数进行动态化
    '''
    #伪装User-Agent作为请求头
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    #实现参数动态化
    params = {
        'query':keyWord
        }
    url = 'https://www.sogou.com/web'
    #params参数（字典）：保存请求时url携带的参数
    response = requests.get(url = url, params = params, headers = headers)
    response.encoding = 'utf-8'
    pageText = response.text
    fileName = keyWord + '.html'
    with open(fileName, 'w', encoding = 'utf-8') as fp:
            fp.write(pageText)
    print(fileName, '爬取成功')
```

* 运行结果：可以正常爬取到关键字的相关数据

> **4. 爬取豆瓣电影详情数据**
>
> * url：<https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C&type=5&interval_id=100:90&action>=
>
* 动态加载数据：
  * 动态加载数据的捕获：使用requests模块爬取数据时无法每次都实现可见即可得
  * 动态加载数据是通过非浏览器地址栏的url请求到的数据，是其他请求请求到的数据
* 如何检测网页中是否存在动态加载数据？
  * 基于抓包工具进行局部搜索
* 如何捕获动态加载的数据
  * 基于抓包工具进行全局搜索（Ctrl+F）
  * ![关键信息全局搜索.png](C:\Users\86199\Pictures\Screenshots\201.png)
  * ![Json格式化.png](C:\Users\86199\Pictures\Screenshots\202.png)
  * 定位动态加载数据对应的数据包
  * 从该数据包中可以提取出：
    * 请求的url
    * 请求的方式
    * 请求的参数
    * 看到响应数据

```python
#首先直接进行爬取
import requests

def favoriteMovie():
    '''
    通过豆瓣爬取一部电影的详细信息
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    url = 'https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C&type=5&interval_id=100:90&action='
    response = requests.get(url = url, headers = headers)
    pageText = response.text
    with open('./douban.html', 'w', encoding = 'utf-8') as fp:
            fp.write(pageText)
```

* 运行结果：
  * 无数据显示
* 原因：
  * 动态加载数据
* 改进：根据上文动态加载数据的捕获方式
  * 定位出数据包并获得url与相关参数

* 爬取成功代码

```python
import requests

def favoriteMovie():
    '''
    通过豆瓣爬取某类排行榜电影的详细信息
    电影名称name、评分score等
    用抓包工具获取所需动态数据数据包相关信息即可
    '''
    #伪装User-Agent作为请求头
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    #定位出动态数据对应数据包的url
    url = 'https://movie.douban.com/j/chart/top_list'
    #字符串参数序列化为字典
    params = {
        'type': '5',
        'interval_id': '100:90',
        'action': '',
        'start': '0',
        'limit': '50',
        }
    response = requests.get(url = url, params = params, headers = headers)
    #.json()将获取的字符串形式的json数据序列化为字典或者列表对象
    pageText = response.json()
    #解析出电影的名称与评分
    for movie in pageText:
        name = movie['title']
        score = movie['score']
        str = name + '\t' + score + '\n'
        with open('./douban.txt', 'a', encoding = 'utf-8') as fp:
            fp.write(str)
```

* 运行结果：
  * ![爬取豆瓣电影名称于评分.png](C:\Users\86199\Pictures\Screenshots\203.png)
  * 可以爬取所需信息
* 问题与思考： 基于抓包工具进行全局搜索不一定每次都能定位到动态加载数据对应的数据包?
  * 如果动态加载的数据是经过加密的密文数据，则无法依赖全局搜索进行定位

> **5. 分页数据的爬取--以爬取肯德基餐厅位置的数据为例**
>
> * url:<http://www.kfc.com.cn/kfccda/storelist/index.aspx>

* 分析：
  * 1. 提交查询关键词后，浏览器发起了一个【**Ajax请求**】(url不变，页面局部内容刷新)
    * Ajax：
      * 概述：它是浏览器提供的一套方法，可以实现页面无刷新更新数据，提高用户浏览网站应用的体验
      * 运行原理：Ajax 相当于浏览器发送请求与接收响应的代理人，以实现在不影响用户浏览页面的情况下，局部更新页面数据，从而提高用户体验
      * 应用场景：
        * 1. 页面上拉加载更多数据
        * 2. 列表数据无刷新分页
        * 3. 表单项离开焦点数据验证
        * 4. 搜索框提示文字下拉列表
  * 2. 当前页面书信出来的位置信息是由Ajax请求到的数据
  * ![Ajax请求数据包相关信息.png](C:\Users\86199\Pictures\Screenshots\204.png)
  * 3. 基于抓包工具定位到该Ajax请求的数据包，从该数据包中捕获到：
    * 请求的url
    * 请求的方式
    * 请求的参数
    * 看到响应数据

* 爬取单页数据

```python
#爬取单页数据
import requests

def pagingCrawl():
    '''
    分页数据的爬取--以爬取肯德基餐厅位置的数据为例
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    data = {
        'cname': '',
        'pid': '',
        'keyword': '北京',
        'pageIndex': '1',
        'pageSize': '10',
        }
    #data是post方法中处理参数动态化的参数
    response = requests.post(url = url, headers = headers, data = data)
    pageText = response.json()
    for dic in pageText['Table1']:
        title = dic['storeName'] + '餐厅'
        addr = dic['addressDetail']
        print(title, addr)
```

* 爬取所有餐厅信息

```python
#爬取所有餐厅信息
import requests

def pagingCrawl():
    '''
    分页数据的爬取--以爬取肯德基餐厅位置的数据为例
    通过for循环对每一次Ajax请求的数据进行爬取并写入
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    for page in range(1, 9):
        data = {
            'cname': '',
            'pid': '',
            'keyword': '北京',
            'pageIndex': str(page),
            'pageSize': '80',
            }
        #data是post方法中处理参数动态化的参数
        response = requests.post(url = url, headers = headers, data = data)
        pageText = response.json()
        #每一页餐厅个数归零
        i = 0

        ## 获取餐厅位置信息， 写入数据
        for dic in pageText['Table1']:
            title = dic['storeName'] + '餐厅'
            addr = dic['addressDetail']
            #记录每页餐厅数目
            i = i + 1
            #统计餐厅总数
            num = str((page - 1) * 10 + i)
            r_str = num + '、 ' + title + '\t' + addr + '\n'
            #创建TXT文件并写入数据
            with open('./restaurant.txt', 'a', encoding = 'utf-8') as fp:
                fp.write(r_str)
```

> **课后作业. 分页数据的爬取--以爬取药监局化妆品企业详细登记信息数据为例**
>
> * 任务：爬取药监总局中的企业详情数据
> * url：<http://scxk.nmpa.gov.cn:81/xk/>
> * 需求：
> >
> > * 将首页中每一家企业的详情数据进行爬取
> >
> * 难点：
> >
> > * 无法全局搜索并爬取到经过加密后的数据
> > * 数据量大，请求过于频繁，服务器端主机拒绝请求

```python
import requests
import json
import time
import socket
def cosmeticsCrawl():
    '''
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
    '''
    
    socket.setdefaulttimeout(20)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}
    ##获取目录页所有企业的名称与id参数
    pre_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    for page in range(1, 370):
        pre_data = {
            'on': 'true',
            'page': str(page),
            'pageSize': '15',
            'productName':'' ,
            'conditionType': '1',
            'applyname': '',
            'applysn':'' ,
            }
        pre_response = requests.post(url = pre_url, headers = headers, data = pre_data)
        pre_response.close()
        pre_pageText = pre_response.json()
        for company in pre_pageText['list']:
            c_name = company['EPS_NAME']
            c_id = company['ID']
            pre_inf = {
                '企业名称':c_name,
                '许可证编号':c_id,
                }
            with open('./pre_company.txt', 'a', encoding = 'utf-8') as f:
                #将字典以Json数据格式写入文件，设置缩进量indent为4
                pre_json_str = json.dump(pre_inf, f, ensure_ascii=False, indent=4)
            ##根据爬取的企业id参数，爬取详情页的企业信息
            url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
            data = {
                'id': c_id
                }
            response = requests.post(url = url, headers = headers, data = data)
            response.close()
            pageText = response.json()
            inf = {
                '企业名称':pageText['epsName'],
                '许可证编号':pageText['productSn'],
                '许可项目':pageText['certStr'],
                '企业住所':pageText['epsAddress'],
                '生产地址':pageText['epsProductAddress'],
                '社会信用代码':pageText['businessLicenseNumber'],
                '法定代表人':pageText['legalPerson'],
                '企业负责人':pageText['businessPerson'],
                '质量负责人':pageText['qualityPerson'],
                '发证机关':pageText['qfManagerName'],
                '签发人':pageText['xkName'],
                '日常监督管理机构':pageText['rcManagerDepartName'],
                '日常监督管理人员':pageText['rcManagerUser'],
                '有效期至':pageText['xkDate'],
                '发证日期':pageText['xkDateStr'],
                '状态':pageText['isimport'],
                '投诉举报电话':str(1233)
                }
            with open('./company.txt', 'a', encoding = 'utf-8') as fp:
                #将字典以Json数据格式写入文件，设置缩进量indent为4
                json_str = json.dump(inf, fp, ensure_ascii=False, indent=4)

            time.sleep(1)
```

# 三、cookie与代理机制

## 1 cookie

### 概要

- cookie：
	- 是存储在客户端的一组键值对
	- Web中cookie的典型应用：
		- 免密登录
	- cookie与爬虫的关联：
		- 有时，不携带cookie对页面进行请求时无法请求到正确的页面数据
		- 因此，cookie是爬虫中一个经典的反爬机制
	
> - **需求1：爬取雪球网的资讯信息**
> 
> - url:<https://xueqiu.com/>

- 分析：
	- 1. 判定所要爬取的数据是否为动态加载
		- 相关的更多数据为动态加载，随着鼠标下拉页面，数据逐步加载
	- 2. 定位到Ajax请求到的数据包，提取请求的url，响应数据为json形式的资讯数据
	
- **问题1：**
	- 请求到的页面数据为错误代码
	
- 原因：
	- 没有按照严格意义上的浏览器行为模拟请求--未携带cookie
	
- 处理：
	- 完全复制浏览器的请求头Request Headers作用到requests的get操作中

- **cookie的处理方式：**
	- 方式1：手动处理
		- 将抓包工具中的cookie直接粘贴在header中
		- 弊端：cookie具有时效性，过了有效时长后会失效
	- 方式2：自动处理
		- 基于Session对象实现自动处理
			- 如何获取一个Session对象：requests.Session()返回一个Session对象
		- Session对象的作用：（首次请求捕获并存储cookie）
			- 该对象可以像requests一样调用get与post发起指定的请求
			- Session发起请求的过程中产生的cookie会被自动存储到对象
			- 即Session的再次请求便为携带cookie的请求
		- 关键：
			- cookie的捕获页面不确定， 需要多次尝试

```python

```

## 2 代理机制

## 3 验证码的识别

## 4 模拟登录
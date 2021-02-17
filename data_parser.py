import requests
import urllib
import bs4


def imageCrawl():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68 '
    }
    img_url = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fa2.att.hudong.com%2F74%2F24' \
              '%2F23300001248577135219240898162.jpg&refer=http%3A%2F%2Fa2.att.hudong.com&app=2002&size=f9999,' \
              '10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1616133427&t=8cc5c8563e57dabed1cf2eeebe33e886 '
    response = requests.get(url=img_url, headers=headers)

    img_data = response.content()
    with open('./1.jpg', 'wb') as fp:
        fp.write(img_data)

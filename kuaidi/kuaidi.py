from lxml import etree

import requests
import lxml
from bs4 import BeautifulSoup
import re


url = 'http://www.tianqi.com/xian'
headers = {
					'Connection': 'Keep-Alive',
					'Accept': 'text/html, application/xhtml+xml, */*',
					'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
html = requests.get(url,headers = headers)
tree = etree.HTML(html.text)
dates = tree.xpath('//ul[@class="week"]/li/b/text()')
weekdays = tree.xpath('//ul[@class="week"]/li/span/text()')
pics = tree.xpath('//ul[@class="week"]/li/img/@src')
temphighs = tree.xpath('//div[@class="zxt_shuju"]/ul/li/span/text()')
templows = tree.xpath('//div[@class="zxt_shuju"]/ul/li/b/text()')
winds = tree.xpath('//ul[@class="txt"]/li/text()')
weathers = tree.xpath('//ul[@class="txt txt2"]/li/text()')
print(str(dates[1]))
print(type(str(dates[1])))

# for i in range(7):
#     print(dates[i])
#     print(weekdays[i])
#     print(pics[i])
#     print(temphighs[i])
#     print(templows[i])
#     print(winds[i])
#     print(weathers[i])
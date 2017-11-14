import requests
import lxml
from bs4 import BeautifulSoup
import re


url = 'http://www.kuaidi100.com/query?type=yunda&postid=1000917880174&temp=0.5763839889703797'
headers = {
					'Connection': 'Keep-Alive',
					'Accept': 'text/html, application/xhtml+xml, */*',
					'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
html = requests.get(url,headers = headers)

print(html.text)

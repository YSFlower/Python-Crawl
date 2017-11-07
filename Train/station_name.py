import requests
import re
from pprint import pprint

# view-source:https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9030
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9030'
requests.packages.urllib3.disable_warnings()
response = requests.get(url,verify=False).text
station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response)
stations = dict(station)
# pprint(dict(station),indent=4)
# def get_url(url):
#     requests.packages.urllib3.disable_warnings()
#
#     r = requests.get(url,verify=False)
#     return r.text


# if __name__ == '__main__':
#     response = get_url('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9030')
#     print(response)
#     station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response)
#     pprint(dict(station), indent=4)
#     print(station.__len__())
#     stations = dict(station)
#     print(stations['德令哈'])

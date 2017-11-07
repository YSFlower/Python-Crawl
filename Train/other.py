#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
from docopt import docopt
from prettytable import PrettyTable

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TrainsCollection(object):
    def __init__(self, available_trains, options, stations):
        self.header = ('车次 车站 时间 历时 特等座 一等 二等 高级软卧 软卧 动卧 硬卧 '
                       + '软座 硬座 无座 备注').split()
        self.available_trains = available_trains
        self.options = options
        self.stations = stations

    # 将历时转化为小时和分钟的形式
    def get_duration(self, raw_train):
        duration = raw_train[10].replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]

        return duration

    # 返回每个车次的基本信息
    def trains(self):
        for raw_train in self.available_trains:
            train_no = raw_train[3]
            initial = train_no[0].lower()

            # 反转station所对应的字典
            stations_re = dict(zip(self.stations.values(), self.stations))
            if not self.options or initial in self.options:
                # 将车次的信息保存到列表中
                train = [
                    train_no,
                    '\n'.join([stations_re.get(raw_train[6]),
                               stations_re.get(raw_train[7])]),
                    '\n'.join([raw_train[8],
                               raw_train[9]]),
                    self.get_duration(raw_train),
                    raw_train[32], raw_train[31], raw_train[30], raw_train[22],
                    raw_train[23], raw_train[33], raw_train[28], raw_train[24],
                    raw_train[29], raw_train[26], raw_train[1]
                ]
                # 更改不运行车次的时间和历时
                if raw_train[14] == 'null':
                    train[2] = '--\n--'
                    train[3] = '--'
                # 将空字符串转化为‘--’
                for i, item in enumerate(train):
                    if not item:
                        train[i] = '--'

                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains():
            pt.add_row(train)

        print(pt)


# 得到station和其大写字母代号相对应的一个字典
def get_stations():
    url_g_s = 'https://kyfw.12306.cn/otn/leftTicket/init'
    resp_g_s = requests.get(url_g_s, verify=False)

    pattern = r'/js/framework/station_name.js?station_version=(\d\.\d+)'
    station_version = re.findall(pattern, resp_g_s.text)

    url_stations = ('https://kyfw.12306.cn/otn/resources/js/framework/station_'
                    + 'name.js?station_version={0}'.format(station_version))

    resp_stations = requests.get(url_stations, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', resp_stations.text)

    return dict(stations)


def main():
    doc = """命令行火车票查看器
Usage:
    tickets.py [-gdtkz] <from> <to> <date>
Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达
Example:
    python tickets.py 北京 上海 2017-11-10
    python tickets.py -dg 成都 南京 2017-11-10
"""

    arguments = docopt(doc)
    stations = get_stations()
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.'
           + 'train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.'
           + 'to_station={2}&purpose_codes=ADULT').format(
        date, from_station, to_station
    )

    r = requests.get(url, verify=False)
    available_trains = r.json()['data']['result']
    available_trains = [i.split('|') for i in available_trains]
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    tickets = TrainsCollection(available_trains, options, stations)
    tickets.pretty_print()


if __name__ == '__main__':
    main()
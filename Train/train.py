# coding = utf-8
"""
命令行火车票查询

Usage:
    train.py [-gdtkz] <from> <to> <date>

Options:
    -h      显示帮助
    -g      高铁
    -d      动车
    -t      特快
    -k      快
    -z      直达

Example：
    train.py -d 北京 上海 2017-11-7

"""
import requests
from docopt import docopt
from prettytable import PrettyTable, ALL, FRAME
from colorama import init,Fore
from station_name import stations
from pprint import pprint

init()

class TrainsCollection:

    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options
        self.stations = stations


    @property
    def trains(self):
        stations_re = {v:k for k,v in stations.items()}
        for raw_train in self.available_trains:
            data_list = raw_train.split('|')

            # 车次号码
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = stations_re[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = stations_re[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30] or '--'
            # 软卧
            soft_sleep = data_list[23] or '--'
            # 硬卧
            hard_sleep = data_list[28] or '--'
            # 硬座
            hard_seat = data_list[29] or '--'
            # 无座
            no_seat = data_list[26] or '--'

            train = [
                train_no,
                '\n'.join([Fore.GREEN + from_station_name + Fore.RESET,
                Fore.RED + to_station_name + Fore.RESET]),
                '\n'.join([Fore.GREEN + start_time + Fore.RESET,
                Fore.RED + arrive_time + Fore.RESET]),
                time_fucked_up,
                first_class_seat,
                second_class_seat,
                soft_sleep,
                hard_sleep,
                hard_seat,
                no_seat,
            ]
            yield train





    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        pt.padding_width = 3
        pt.hrules = ALL
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # print(arguments)
    # print(from_station)
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)
    # print(url)
    r = requests.get(url,verify=False)
    r.encoding = 'utf-8'
    # print(r.json())
    available_trains = r.json()['data']['result']
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    TrainsCollection(available_trains, options).pretty_print()
    # pprint(available_trains,indent=2)

if __name__ == '__main__':
    cli()

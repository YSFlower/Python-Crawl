# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import json
import codecs
import pymysql

class WeatherPipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = os.path.join(base_dir,'data','weather.txt')

        with open(filename,'a') as f:
            f.write(item['date'] + '\n')
            f.write(item['weekday'] + '\n')
            f.write(item['temp'] + '\n')
            f.write(item['weather'] + '\n')
            f.write(item['wind'] + '\n\n')
        with open(base_dir + '/data/' + item['date'] + '.png','wb') as f:
            f.write(requests.get('https://www.tianqi.com' + item['image']).content)

        return item

class W2json(object):
    def process_item(self,item,spider):
        base_dir = os.getcwd()
        filename = os.path.join(base_dir,'data','weather.json')
        print('--------------------------------')
        print(item)
        with codecs.open(filename,'a') as f:
            line = json.dumps(dict(item),ensure_ascii=False) + '\n'
            f.write(line)

        return item


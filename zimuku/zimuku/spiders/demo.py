# -*- coding: utf-8 -*-
import scrapy
from zimuku.items import ZimukuItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['http://zimuku.net']
    start_urls = ['http://http://zimuku.net/']

    def parse(self, response):
        '''
        parse()函数接收Response参数，就是网页爬取后返回的数据
        用于处理相应，负责解析爬取的内容
        生成解析结果的字典，并返回新的需要爬取的请求
        '''
       	name = response.xpath('//b/text()').extract()[1]
       	item = {}
       	item['第一个'] = name

       	return items

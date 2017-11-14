# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class XatianqiSpider(scrapy.Spider):
    name = 'XAtianqi'
    allowed_domains = ['tianqi.com/xian/']
    start_urls = ['http://tianqi.com/xian/']

    def parse(self, response):
        items = []
        dates = response.xpath('//ul[@class="week"]/li/b/text()').extract()
        weekdays = response.xpath('//ul[@class="week"]/li/span/text()').extract()
        pics = response.xpath('//ul[@class="week"]/li/img/@src').extract()
        temphighs = response.xpath('//div[@class="zxt_shuju"]/ul/li/span/text()').extract()
        templows = response.xpath('//div[@class="zxt_shuju"]/ul/li/b/text()').extract()
        weathers = response.xpath('//ul[@class="txt txt2"]/li/text()').extract()
        winds = response.xpath('//ul[@class="txt"]/li/text()').extract()

        for i in range(7):
            item = WeatherItem()
            item['date'] = str(dates[i])
            item['weekday'] = str(weekdays[i])
            item['image'] = str(pics[i])
            item['temp'] = str(temphighs[i]) + ' ~ ' + str(templows[i]) + '℃'
            # item['temphigh'] = temphighs[i]
            # item['templow'] = templows[i]
            item['weather'] = str(weathers[i])
            item['wind'] = str(winds[i])
            items.append(item)
        return items

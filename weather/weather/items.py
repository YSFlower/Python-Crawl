# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    weekday = scrapy.Field()
    image = scrapy.Field()
    temp = scrapy.Field()
    weather = scrapy.Field()
    wind = scrapy.Field()
    pass


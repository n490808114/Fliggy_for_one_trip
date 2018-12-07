# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FliggyjsonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    depcity = scrapy.Field()
    arrcity = scrapy.Field()
    depdate = scrapy.Field()
    airlineInfo = scrapy.Field()
    depAirportName = scrapy.Field()
    arrAirportName = scrapy.Field()
    depTimeStr = scrapy.Field()
    arrTimeStr = scrapy.Field()
    price = scrapy.Field()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import datetime
from openpyxl import Workbook

class FliggyjsonPipeline(object):
    def __init__(self):
        filename = str(datetime.datetime.now()).split('.')[0].replace(':','_')
        self.file = codecs.open(f'{filename}.json','wb',encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def close_spider(self,spider):
        self.file.close()

class FliggyxlsxPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['起飞城市','到达城市','起飞日期','航班信息','起飞机场','到达机场','起飞时间','到达时间','价格'])
    def process_item(self, item, spider):
        line = [item["depcity"],item["arrcity"],item["depdate"],item["airlineInfo"],item["depAirportName"],item["arrAirportName"],item["depTimeStr"],item["arrTimeStr"],item["price"]]
        self.ws.append(line)
        return item
    def close_spider(self, spider):
        filename = str(datetime.datetime.now()).split('.')[0].replace(':','_')
        self.wb.save(f"{filename}.xlsx")

    
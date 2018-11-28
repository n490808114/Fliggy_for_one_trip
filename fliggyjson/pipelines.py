# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import time

class FliggyjsonPipeline(object):
    def __init__(self):
        self.file = codecs.open(f'{int(time.time()*1000)}.json','wb',encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_close(self,spider):
        self.file.close()
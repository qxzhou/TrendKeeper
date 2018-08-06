# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs

class MysolutionPipeline(object):
    def __init__(self):
        self.file = codecs.open('test.json', 'w', encoding='utf-8')


    def close_spider(self, spider):
        self.file.close()

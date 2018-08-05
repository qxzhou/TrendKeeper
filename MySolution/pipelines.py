# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs

class MysolutionPipeline(object):
    def __init__(self):
        self.file = codecs.open('rawdata.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        """
        Save the data into json file
        """

        # get data from item
        # data is stored in tuple
        category = item['category'],
        date = item['date'],
        keyword = item['keyword'],
        location = item['location'],

        print ('Look at items cate %s ' % type(category))
        #add ,
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()

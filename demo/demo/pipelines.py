# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook

class DemoPipeline(object):
    def __init__(self):
        self.wb=Workbook()
        self.ws=self.wb.active
        self.ws.append(['总价','单价','户型'])

    def process_item(self, item, spider):
        line=[item['title'],item['area'],item['roomtype']]
        print(line)
        return item

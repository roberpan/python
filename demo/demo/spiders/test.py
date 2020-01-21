# -*- coding: utf-8 -*-
import scrapy
from demo.items import DemoItem

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/ershoufang/']

    def parse(self, response):
        item=DemoItem()
        contents=response.css('div.info.clear')
        for content in contents:
            item['title']=content.css('.title a::text').extract()[0]
            item['area']=content.css('.houseInfo::text').extract()[0].split(' | ')[1]
            item['roomtype']=content.css('.houseInfo::text').extract()[0].split(' | ')[0]


